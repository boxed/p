module Main where

-- System Modules
import System.FilePath.Posix (pathSeparator) -- / for Linux/OS X and \ for Windows
import Text.Printf (printf)
import System.Environment
import Data.List.Split
import System.Process as Process
-- Custom Modules
import Project
import Call (call)
import Config (p_config,p_folder,ls_command,execute_cmd) -- Config variables

main = do
  -- p Commands:
  -- Every p Command follows this scheme:
  -- p <language> <command>
  -- The <language> part should be omitted, if p can auto detect
  -- the directory structure (execute p, without any arguments to see what project type p detects).
  -- TODO: Not yet implemented auto-detect

  -- p <language> <command> <args>
  args <- getArgs

  let language = (args !! 0) -- TODO: implement auto_detect
      command = if language /= (args !! 0) then (args !! 0) else (args !! 1) -- if didn't auto detect work, use args !! 1
  {-
     Packages are folders in the ~/.p/packages directory
     ~/.p/packages/
     ├── go
     ├── python
     └── swift
     Each one of these in turn has one executable for each <command>:
     python/
     ├── install
     ├── remove
     ├── repl
     └── run
     If you execute the command:
     p python install <pip-package>
     p would execute ~/.p/packages/python/install <pip-package>.
     ( The .p Folder path is in the p_folder variable).
  -}
  Process.callProcess (execute_cmd ++ (create_path [p_folder,"packages",language,command])) [] -- Execute command without caputring output
