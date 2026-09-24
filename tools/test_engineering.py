"""工程回归：安全目录、错误传播、显式模块、安装幂等；夹具全部位于临时目录。"""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "shared" / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StructureTests(unittest.TestCase):
    def check(self, content, required=(), **extra):
        spec = {"qa": {"profile": "short", "requiredModules": list(required)}, "content": content}
        spec["qa"].update(extra.get("qa", {}))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
            args = [sys.executable, str(SCRIPTS / "structure_qa.py"), str(path)]
            if extra.get("pdf"):
                args += ["--pdf", str(Path(tmp) / "missing.pdf")]
            return subprocess.run(args, text=True, capture_output=True)

    def test_short_disclosures_are_valid(self):
        result = self.check([["p", "用户提供资料；数据缺口待补充，估值待核实、待校准；目标为建议值，非预测。"]])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_declared_modules_fail(self):
        result = self.check([], ["qa", "suitability", "battlecard"])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.count("缺少声明的必要模块"), 3)

    def test_renamed_question_table_keeps_row_requirement(self):
        table = {"module": "qa", "head": ["顾虑", "表达"], "rows": [["为何", "如此"]] * 9}
        self.assertIn("FAIL F5", self.check([["t", table]], ["qa"]).stdout)
        table["rows"].append(["为何", "如此"])
        self.assertEqual(self.check([["t", table]], ["qa"]).returncode, 0)

    def test_renamed_suitability_and_battlecard(self):
        fit = {"module": "suitability", "head": ["需求", "结论"], "rows": [["短钱", "不适合"], ["已有", "匹配度有限"]]}
        battle = {"module": "battlecard", "head": ["角度", "论据", "代价"], "acknowledgementColumn": 2, "rows": [["费用", "倾斜", "比同业贵"]]}
        content = [["t", fit], ["s", "资料来源：本报告整理"], ["t", battle], ["s", "资料来源：本报告整理"]]
        self.assertEqual(self.check(content, ["suitability", "battlecard"]).returncode, 0)
        battle["rows"][0][2] = ""
        self.assertIn("FAIL F7", self.check(content, ["battlecard"]).stdout)
        del battle["acknowledgementColumn"]
        self.assertIn("缺少可识别的承认栏", self.check(content, ["battlecard"]).stdout)

    def test_partial_questions_follow_confirmed_scope(self):
        table = {"module": "qa", "head": ["顾虑", "表达"], "rows": [["为何", "如此"]] * 3}
        content = [["t", table], ["s", "资料来源：本报告建议"]]
        self.assertEqual(self.check(content, ["qa"], qa={"minQuestions": 3}).returncode, 0)
        self.assertEqual(self.check(content, ["qa"]).returncode, 1)
        self.assertNotEqual(self.check(content, ["qa"], qa={"profile": "report", "minQuestions": 3}).returncode, 0)
        self.assertNotEqual(self.check(content, ["qa"], qa={"minQuestions": 0}).returncode, 0)

    def test_empty_source_is_not_a_source(self):
        self.assertEqual(self.check([["s", "资料来源："]]).returncode, 1)
        self.assertEqual(self.check([["f", {"src": "资料来源：", "cap": "图"}]]).returncode, 1)

    def test_requested_pdf_cannot_silently_skip(self):
        result = self.check([], pdf=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("未实测", result.stdout)

    def test_legacy_example_still_passes(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / "structure_qa.py"), str(ROOT / "shared/examples/polaris-mini.json"), "--example"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class SummaryPdfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load("structure_qa")
        cls.next_title = "第一章　它不是三十只等权篮子：三家核心加二十七只卫星"

    def mock_pages(self, pages):
        def run(args, **kwargs):
            text = f"Pages: {len(pages)}\n" if args[0] == "pdfinfo" else pages[int(args[args.index("-f") + 1]) - 1]
            return subprocess.CompletedProcess(args, 0, text, "")
        return patch.object(self.module.subprocess, "run", side_effect=run)

    def test_moved_toc_and_summary_reference_do_not_match_as_chapter(self):
        pages = ["封面", "封面声明续页", "页眉\n目\n录\n执行摘要\n" + self.next_title,
                 "页眉\n执行摘要\n下章将说明：" + self.next_title,
                 "页眉\n摘要续页。它不是三十只等权篮子，但此处不是章标题。",
                 "页眉\n第一章\n内部参考\n它不是三十只等权篮子：\n三家核心加二十七只卫星\n正文"]
        with self.mock_pages(pages):
            self.assertEqual(self.module.locate_summary_pages("fixture.pdf", "执行摘要", self.next_title, ["页眉", "内部参考"]), (4, 6))

    def test_missing_full_title_remains_unmeasured(self):
        for pages in [["执行摘要\n正文", "第一章　它不是三十只等权篮子：截断标题"], ["没有摘要", self.next_title]]:
            with self.subTest(pages=pages), self.mock_pages(pages):
                self.assertIsNone(self.module.locate_summary_pages("fixture.pdf", "执行摘要", self.next_title)[1])

    def test_summary_spanning_three_pages_is_measured(self):
        with self.mock_pages(["封面", "执行摘要\n正文", "续页1", "续页2", self.next_title]):
            self.assertEqual(self.module.locate_summary_pages("fixture.pdf", "执行摘要", self.next_title), (2, 5))

    def check_main_measurement(self, positions):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            pdf = Path(tmp) / "report.pdf"
            report.write_text(json.dumps({"qa": {"profile": "short"}, "content": [["h1", "执行摘要"], ["h1", self.next_title]]}, ensure_ascii=False), encoding="utf-8")
            pdf.write_bytes(b"fixture")
            output = io.StringIO()
            with patch.object(sys, "argv", ["structure_qa.py", str(report), "--pdf", str(pdf)]), patch.object(self.module.shutil, "which", return_value="tool"), patch.object(self.module, "locate_summary_pages", return_value=positions), contextlib.redirect_stdout(output):
                with self.assertRaises(SystemExit) as done:
                    self.module.main()
            return done.exception.code, output.getvalue()

    def test_zero_negative_or_missing_pages_warn_without_fake_measurement(self):
        for positions in [(3, 3), (4, 3), (4, None), (None, None)]:
            with self.subTest(positions=positions):
                code, output = self.check_main_measurement(positions)
                self.assertEqual(code, 0)
                self.assertIn("WARN W2", output)
                self.assertIn("页数未实测", output)
                self.assertNotIn("[执行摘要]", output)

    def test_summary_exceeding_two_pages_fails(self):
        code, output = self.check_main_measurement((2, 5))
        self.assertEqual(code, 1)
        self.assertIn("执行摘要占 3 页", output)


class TextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load("text_qa")

    def check(self, text):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = self.module.check_text(text)
        return code, output.getvalue()

    def test_hard_errors_fail(self):
        for text in ["TODO", "**残留**", "资料来源：", "样例机构"]:
            with self.subTest(text=text):
                self.assertEqual(self.check(text)[0], 1)

    def test_caution_has_context_and_does_not_ban_risk_disclosure(self):
        code, output = self.check("本产品不保本，不保证收益。\n数据缺口待核实；待补数据、待校准假设均已记录；目标为建议值。")
        self.assertEqual(code, 0)
        self.assertIn("WARN 慎用词", output)
        self.assertIn("本产品不保本", output)
        self.assertIn("0 FAIL", output)

    def test_extraction_failure_and_empty_output_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.docx"
            path.write_bytes(b"fixture")
            with patch.object(self.module.shutil, "which", return_value="pandoc"):
                with patch.object(self.module.subprocess, "run", side_effect=subprocess.CalledProcessError(4, ["pandoc"])):
                    with self.assertRaises(subprocess.CalledProcessError):
                        self.module.main([str(path)])
                with patch.object(self.module.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")):
                    with self.assertRaises(RuntimeError):
                        self.module.main([str(path)])


class RenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load("render_qa")

    def fake_pdf(self, source, directory):
        path = Path(directory) / "in.pdf"
        path.write_bytes(b"pdf fixture")
        return str(path)

    def fake_render(self, args, **kwargs):
        from PIL import Image
        Image.new("RGB", (20, 30), "white").save(args[-1] + "-1.png")
        return subprocess.CompletedProcess(args, 0)

    def test_repeated_same_directory_preserves_input_and_other_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "report.docx"
            sentinel = Path(tmp) / "original.txt"
            source.write_bytes(b"original report")
            sentinel.write_text("must survive", encoding="utf-8")
            with patch.object(self.module, "to_pdf", side_effect=self.fake_pdf), patch.object(self.module.shutil, "which", return_value="pdftoppm"), patch.object(self.module.subprocess, "run", side_effect=self.fake_render), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(self.module.main([str(source), tmp]), 0)
                self.assertEqual(self.module.main([str(source), tmp]), 0)
                self.assertEqual(self.module.main([str(source), "--zoom", "1"]), 0)
            self.assertEqual(source.read_bytes(), b"original report")
            self.assertEqual(sentinel.read_text(), "must survive")
            self.assertEqual(len(list(Path(tmp).glob("run-*"))), 2)
            self.assertEqual(len(list((Path(tmp) / "render_qa").glob("run-*"))), 1)

    def test_conversion_failure_propagates(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(self.module.shutil, "which", return_value="soffice"), patch.object(self.module.subprocess, "run", side_effect=subprocess.CalledProcessError(8, ["soffice"])) as run:
            with self.assertRaises(subprocess.CalledProcessError):
                self.module.to_pdf(str(Path(tmp) / "in.docx"), tmp)
            self.assertTrue(run.call_args.kwargs["check"])

    def test_invalid_zoom_is_rejected(self):
        with self.assertRaises(Exception):
            self.module.zoom_pages("0,abc")

    def test_mac_fontconfig_uses_existing_app_config_without_global_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = Path(tmp) / "Contents/MacOS/soffice"
            config = Path(tmp) / "Contents/Resources/fontconfig/fonts.conf"
            binary.parent.mkdir(parents=True)
            binary.write_text("fixture")
            config.parent.mkdir(parents=True)
            config.write_text("<fontconfig/>")
            with patch.object(self.module.sys, "platform", "darwin"), patch.object(self.module.shutil, "which", return_value=str(binary)), patch.dict(os.environ, {}, clear=True):
                env = self.module.conversion_env(str(binary))
                self.assertEqual(env["FONTCONFIG_FILE"], str(config.resolve()))
                self.assertNotIn("FONTCONFIG_FILE", os.environ)
                with patch.object(self.module.sys, "platform", "linux"):
                    self.assertNotIn("FONTCONFIG_FILE", self.module.conversion_env(str(binary)))
                with patch.dict(os.environ, {"FONTCONFIG_FILE": "/user/chosen.conf"}):
                    self.assertEqual(self.module.conversion_env(str(binary))["FONTCONFIG_FILE"], "/user/chosen.conf")


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.repo = self.base / "repo"
        (self.repo / "tools").mkdir(parents=True)
        shutil.copy2(ROOT / "tools/install_codex.sh", self.repo / "tools/install_codex.sh")
        for directory in ["shared/scripts", "skills/alpha/scripts", "skills/beta"]:
            (self.repo / directory).mkdir(parents=True)
        for directory in ["shared/scripts", "skills/alpha/scripts"]:
            (self.repo / directory / "package.json").write_text("{}")
        (self.repo / "shared/scripts/doctor.py").write_text("raise SystemExit(0)\n")
        self.bin = self.base / "bin"
        self.bin.mkdir()
        for name in ["npm", "node"]:
            executable = self.bin / name
            executable.write_text("#!" + sys.executable + "\nimport os,sys\nfrom pathlib import Path\nwith open(os.environ['INSTALL_TEST_LOG'],'a') as f: f.write(Path(sys.argv[0]).name+' '+repr(sys.argv[1:])+'\\n')\nraise SystemExit(7 if os.environ.get('INSTALL_TEST_FAIL') == Path(sys.argv[0]).name else 0)\n")
            executable.chmod(0o755)
        self.dest = self.base / "installed"
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ["PATH"], INSTALL_TEST_LOG=str(self.base / "commands.log"))

    def run_install(self):
        return subprocess.run(["bash", str(self.repo / "tools/install_codex.sh"), str(self.dest)], env=self.env, text=True, capture_output=True)

    def test_install_is_idempotent_and_installs_each_entry(self):
        for _ in range(2):
            result = self.run_install()
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.dest / "alpha").resolve(), (self.repo / "skills/alpha").resolve())
        log = (self.base / "commands.log").read_text()
        self.assertIn(str(self.repo / "shared/scripts"), log)
        self.assertIn(str(self.repo / "skills/alpha/scripts"), log)

    def test_existing_directory_or_unrelated_link_is_preserved(self):
        self.dest.mkdir()
        target = self.dest / "beta"
        target.mkdir()
        sentinel = target / "mine.txt"
        sentinel.write_text("keep")
        self.assertNotEqual(self.run_install().returncode, 0)
        self.assertEqual(sentinel.read_text(), "keep")
        self.assertFalse((self.dest / "alpha").exists())
        target.rename(self.base / "old-beta")
        target.symlink_to(self.base / "old-beta")
        self.assertNotEqual(self.run_install().returncode, 0)
        self.assertEqual(target.resolve(), (self.base / "old-beta").resolve())

    def test_failed_dependency_install_does_not_claim_completion(self):
        self.env["INSTALL_TEST_FAIL"] = "npm"
        result = self.run_install()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("完成。", result.stdout)
        self.assertFalse(self.dest.exists())


if __name__ == "__main__":
    unittest.main()
