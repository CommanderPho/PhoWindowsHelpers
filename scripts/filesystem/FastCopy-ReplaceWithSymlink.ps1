# Define your variables
$Source = "C:\Path\To\Source"
$Destination = "D:\Path\To\Destination"

# 1. Run FastCopy silently to copy the files
& "C:\Program Files\FastCopy\FastCopy.exe" /cmd=copy /auto_close /no_confirm_del $Source /to=$Destination

# 2. Run the post-process action
& "scripts\filesystem\helpers\FastCopy-Symlink.ps1" -SourceString $Source -DestinationDir $Destination

