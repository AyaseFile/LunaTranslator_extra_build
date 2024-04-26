import argparse
import os
import shutil
import subprocess

py37Path32 = os.path.join(
    os.environ["LOCALAPPDATA"], "Programs\\Python\\Python37-32\\python.exe"
)
py37Path64 = os.path.join(
    os.environ["LOCALAPPDATA"], "Programs\\Python\\Python37\\python.exe"
)
py311Path = os.path.join(
    os.environ["LOCALAPPDATA"], "Programs\\Python\\Python311\\python.exe"
)
msbuildPath = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\MSBuild\\Current\\Bin\\MSBuild.exe"
vcvars32Path = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\VC\\Auxiliary\\Build\\vcvars32.bat"
vcvars64Path = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\VC\\Auxiliary\\Build\\vcvars64.bat"

pluginDirs = ["DLL32", "DLL64", "Locale_Remulator", "LunaHook", "Magpie", "NTLEAS"]

vcltlFile = "https://github.com/Chuyu-Team/VC-LTL5/releases/download/v5.0.9/VC-LTL-5.0.9-Binary.7z"
vcltlFileName = "VC-LTL-5.0.9-Binary.7z"
brotliFile32 = "https://github.com/google/brotli/releases/latest/download/brotli-x86-windows-dynamic.zip"
brotliFileName32 = "brotli-x86-windows-dynamic.zip"
brotliFile64 = "https://github.com/google/brotli/releases/latest/download/brotli-x64-windows-dynamic.zip"
brotliFileName64 = "brotli-x64-windows-dynamic.zip"
localeEmulatorFile = "https://github.com/xupefei/Locale-Emulator/releases/download/v2.5.0.1/Locale.Emulator.2.5.0.1.zip"
localeEmulatorFileName = "Locale.Emulator.2.5.0.1.zip"
ntleaFile = "https://github.com/zxyacb/ntlea/releases/download/0.46/ntleas046_x64.7z"
ntleaFileName = "ntleas046_x64.7z"
curlFile32 = "https://curl.se/windows/dl-8.7.1_7/curl-8.7.1_7-win32-mingw.zip"
curlFileName32 = "curl-8.7.1_7-win32-mingw.zip"
curlFile64 = "https://curl.se/windows/dl-8.7.1_7/curl-8.7.1_7-win64-mingw.zip"
curlFileName64 = "curl-8.7.1_7-win64-mingw.zip"
onnxruntimeFile = "https://github.com/RapidAI/OnnxruntimeBuilder/releases/download/1.14.1/onnxruntime-1.14.1-vs2019-static-mt.7z"
onnxruntimeFileName = "onnxruntime-1.14.1-vs2019-static-mt.7z"
opencvFile = "https://github.com/RapidAI/OpenCVBuilder/releases/download/4.7.0/opencv-4.7.0-windows-vs2019-mt.7z"
opencvFileName = "opencv-4.7.0-windows-vs2019-mt.7z"

mecabUrl = "https://github.com/HIllya51/mecab.git"
webviewUrl = "https://github.com/HIllya51/webview.git"
localeRemulatorUrl = "https://github.com/HIllya51/Locale_Remulator.git"
lunaHookUrl = "https://github.com/HIllya51/LunaHook.git"
magpieUrl = "https://github.com/HIllya51/Magpie_CLI.git"
lunaOCRUrl = "https://github.com/HIllya51/LunaOCR.git"

ocrModelUrl = "https://github.com/HIllya51/RESOURCES/releases/download/ocr_models"
availableLocales = ["cht", "en", "ja", "ko", "ru", "zh"]


rootDir = os.path.dirname(__file__)


def installVCLTL():
    os.chdir(rootDir + "\\temp")
    subprocess.run(f"curl -LO {vcltlFile}")
    subprocess.run(f"7z x {vcltlFileName} -oVC-LTL5")
    os.chdir("VC-LTL5")
    subprocess.run("cmd /c Install.cmd")


def buildMecab():
    os.chdir(rootDir + "\\temp")
    subprocess.run(f"git clone {mecabUrl}")
    os.chdir("mecab\\mecab")

    
    os.makedirs(f"{rootDir}/ALL/DLL32",exist_ok=True)
    os.makedirs(f"{rootDir}/ALL/DLL64",exist_ok=True)
    subprocess.run(f'cmd /c "{vcvars32Path}" & call make.bat')
    shutil.move("src/libmecab.dll", f"{rootDir}/ALL/DLL32")

    subprocess.run(f'cmd /c "{vcvars64Path}" & call makeclean.bat & call make.bat')
    shutil.move("src/libmecab.dll", f"{rootDir}/ALL/DLL64")


def buildWebview():
    os.chdir(rootDir + "\\temp")
    subprocess.run(f"git clone {webviewUrl}")
    os.chdir("webview\\script")
    os.makedirs(f"{rootDir}/ALL/DLL32",exist_ok=True)
    os.makedirs(f"{rootDir}/ALL/DLL64",exist_ok=True)
    subprocess.run(f"cmd /c set TARGET_ARCH=x86 & call build.bat")
    shutil.move(
        "../build/library/webview.dll", f"{rootDir}/ALL/DLL32"
    )
    subprocess.run(f"cmd /c set TARGET_ARCH=x64 & call build.bat")
    shutil.move(
        "../build/library/webview.dll", f"{rootDir}/ALL/DLL64"
    )


def buildLocaleRemulator():
    os.chdir(rootDir + "\\temp")
    subprocess.run(f"git clone {localeRemulatorUrl}")
    os.chdir("Locale_Remulator")
    subprocess.run(f"nuget restore")
    os.chdir("LRHook")
    os.makedirs(f"{rootDir}/ALL/Locale_Remulator",exist_ok=True)
    subprocess.run(
        f'"{msbuildPath}" LRHook.vcxproj /p:Configuration=Release /p:Platform=x86'
    )
    shutil.move(
        "x64/Release/LRHookx32.dll",
        f"{rootDir}/ALL/Locale_Remulator",
    )
    subprocess.run(
        f'"{msbuildPath}" LRHook.vcxproj /p:Configuration=Release /p:Platform=x64'
    )
    shutil.move(
        "x64/Release/LRHookx64.dll",
        f"{rootDir}/ALL/Locale_Remulator",
    )



def buildLunaOCR():
    os.chdir(rootDir + "\\temp")
    subprocess.run(f"git clone {lunaOCRUrl}")
    os.chdir("LunaOCR")
    os.chdir("onnxruntime-static")
    subprocess.run(f"curl -LO {onnxruntimeFile}")
    subprocess.run(f"7z x {onnxruntimeFileName}")
    os.chdir("..")
    os.chdir("opencv-static")
    subprocess.run(f"curl -LO {opencvFile}")
    subprocess.run(f"7z x {opencvFileName}")
    os.chdir("..")

    buildType = "Release"
    buildOutput = "CLIB"
    mtEnabled = "True"
    onnxType = "CPU"
    toolset = "v143"
    arch32 = "Win32"
    arch64 = "x64"

    os.makedirs(f"build/win-{buildOutput}-{onnxType}-{arch32}")
    os.chdir(f"build/win-{buildOutput}-{onnxType}-{arch32}")
    subprocess.run(
        f'cmake -T "{toolset},host=x64" -A {arch32} '
        f"-DCMAKE_INSTALL_PREFIX=install "
        f"-DCMAKE_BUILD_TYPE={buildType} -DOCR_OUTPUT={buildOutput} "
        f"-DOCR_BUILD_CRT={mtEnabled} -DOCR_ONNX={onnxType} ../.."
    )
    subprocess.run(f"cmake --build . --config {buildType} -j {os.cpu_count()}")
    subprocess.run(f"cmake --build . --config {buildType} --target install")

    os.chdir(f"{rootDir}/temp/LunaOCR")

    os.makedirs(f"build/win-{buildOutput}-{onnxType}-{arch64}")
    os.chdir(f"build/win-{buildOutput}-{onnxType}-{arch64}")
    subprocess.run(
        f'cmake -T "{toolset},host=x64" -A {arch64} '
        f"-DCMAKE_INSTALL_PREFIX=install "
        f"-DCMAKE_BUILD_TYPE={buildType} -DOCR_OUTPUT={buildOutput} "
        f"-DOCR_BUILD_CRT={mtEnabled} -DOCR_ONNX={onnxType} ../.."
    )
    subprocess.run(f"cmake --build . --config {buildType} -j {os.cpu_count()}")
    subprocess.run(f"cmake --build . --config {buildType} --target install")

    os.chdir(f"{rootDir}/temp/LunaOCR")
    os.makedirs(f"{rootDir}/ALL/DLL32",exist_ok=True)
    os.makedirs(f"{rootDir}/ALL/DLL64",exist_ok=True)
    shutil.move(
        f"build/win-{buildOutput}-{onnxType}-{arch32}/install/bin/LunaOCR32.dll",
        f"{rootDir}/ALL/DLL32",
    )
    shutil.move(
        f"build/win-{buildOutput}-{onnxType}-{arch64}/install/bin/LunaOCR64.dll",
        f"{rootDir}/ALL/DLL64",
    )


def buildMagpie():
    os.chdir(rootDir + "\\temp")
    subprocess.run(f"git clone {magpieUrl}")
    os.chdir("Magpie_CLI")
    subprocess.run(
        f'"{msbuildPath}" -restore -p:RestorePackagesConfig=true;Configuration=Release;Platform=x64;OutDir={os.getcwd()}\\publish\\x64\\ Magpie.sln'
    )
    os.makedirs(f"{rootDir}/ALL/Magpie", exist_ok=True)
    shutil.move("publish/x64/Magpie.Core.exe", f"{rootDir}/ALL/Magpie")
    shutil.move("publish/x64/effects", f"{rootDir}/ALL/Magpie")


def installDependencies():
    os.chdir(rootDir)
    subprocess.run(f"{py311Path} -m pip install --upgrade pip")
    subprocess.run(f"{py311Path} -m pip install conan cmake pefile")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-download",
        action="store_true",
        default=False,
        help="Skip download steps",
    )
    parser.add_argument(
        "--skip-python-dependencies",
        action="store_true",
        default=False,
        help="Skip Python dependencies installation",
    )
    parser.add_argument(
        "--skip-vc-ltl",
        action="store_true",
        default=False,
        help="Skip VC-LTL installation",
    )
    parser.add_argument(
        "--skip-build", action="store_true", default=False, help="Skip build steps"
    )
    parser.add_argument(
        "--clean-temp",
        action="store_true",
        default=False,
        help="Clean temp directory before building",
    )
    parser.add_argument(
        "--clean-plugins",
        action="store_true",
        default=False,
        help="Clean plugins directory before building",
    )
    parser.add_argument(
        "--github-actions",
        action="store_true",
        default=False,
        help="Specify if running in a GitHub Actions environment",
    )

    args = parser.parse_args()

    os.chdir(rootDir)
    if args.clean_temp:
        os.system('powershell.exe -Command "Remove-Item -Path .\\temp -Recurse -Force"')
    if not os.path.exists("temp"):
        os.mkdir("temp")


    if args.github_actions:
        py311Path = "C:\\hostedtoolcache\\windows\\Python\\3.11.7\\x64\\python.exe"

    if not args.skip_python_dependencies:
        installDependencies()
    if not args.skip_build:
        if not args.skip_vc_ltl:
            installVCLTL()
        buildMecab()
        buildWebview()
        buildLocaleRemulator()
        buildLunaOCR()
        buildMagpie()

    
    os.chdir(rootDir)
    os.system(rf'"C:\Program Files\7-Zip\7z.exe" a -m0=LZMA -mx9 .\\ALL.zip .\\ALL')

    subprocess.run(f"curl -LO https://github.com/tcnksm/ghr/releases/download/v0.16.2/ghr_v0.16.2_windows_amd64.zip")
    subprocess.run(f"7z x ghr_v0.16.2_windows_amd64.zip")
    subprocess.run(f'ghr_v0.16.2_windows_amd64/ghr -u HIllya51 -r LunaTranslator_extra_build -replace common ALL.zip')
          