module Config where
-- Build Configurations
-- Don't mix logic and Configuration!
import System.Info (os)

unix  = os == "darwin" || os == "linux"

-- I don't know if the windows command is right. But for linux and OS X, it is right
ls_command = if unix then "ls " else "dir "

-- Again, I don't know about Windows
p_config = if unix then "~/.pconfig" else "~\\.pconfig"

-- Again, I don't know about Windows
p_folder = if unix then "~/.p" else "~\\.p"

-- Execute a command on the specific machine
execute_cmd = if unix then "" else ""
