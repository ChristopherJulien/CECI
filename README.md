# Combined-Environment-Control-Interface
Combined Environment Control Interface

# Installation Process
1. clone/download this repository
2. Open a powershell with admin right on the folder where the repository was cloned (accept the prompt to open admin acces)
3. Go to the folder python-image
4. Give the installation batch access to run with admin rights by running on the command line ```Set-ExecutionPolicy RemoteSigned```

# Windows Driver and Program Setup <img height=20 src="documentation/media/windows_logo.png"/>
1. Once in the folder Combined-Environment-Control-Interface\python-image run the powershell commands ``` ./install_all.ps1 ```
-1. If you get the error:
```\install_all.ps1 cannot be loaded 
because running scripts is disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ .\install_all.ps1
+ ~~~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess ```

you may be attempting to run the installation without admin rights. Please refer to step #4 of _Installation Process_

2. Follow the installation wizard to install logic 
3. You should see ``` Driver Setup.exe executed successfully.``` appear on the console

# Bulid the Python Developer Setup <img height=20 src="documentation/media/docker_logo.png"/>
1.Download docker image

# Run the Python Developer Setup <img height=20 src="documentation/media/python_logo.png"/>
1. Run docker Imge with this command
2.
3.
