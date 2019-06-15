module Main where

-- System Modules
import System.FilePath.Posix (pathSeparator) -- / for Linux/OS X and \ for Windows
import Text.Printf (printf)

-- Custom Modules
import Call (call)
import Config (P_MATCHES,P_CONFIG,P_FOLDER) -- Config variables

main :: IO ()
main = do
  -- p Commands:
  -- Every p Command follows this scheme:
  -- p <language> <command>
  -- The <language> part should be omitted, if p can auto detect
  -- the directory structure (execute p, without any arguments to see what project type p detects).
  -- TODO: Not yet implemented auto-detect

  -- p <language> <command> <args>
  args <- getArgs

  -- Detect the project and if that is not possible, use args[0]
  language <- auto_detect args[0]

  -- If auto detection worked, use args[1], else args[0]
  let command = if language /= args[0] then args[0] else args[1]

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
     ( The .p Folder path is in the P_FOLDER variable).
  -}
  output <- call $ join pathSeparator [".",P_FOLDER,"packages",language,command] -- Command executes
