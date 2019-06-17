module Project
    (
     auto_detect,
     create_path
     ) where

-- stdlib Modules
import Text.Regex.Posix
import System.IO
import System.FilePath.Posix (pathSeparator)
import Data.List
-- p Modules
import Call (call)
import Config (ls_command,p_folder) -- ls_command: equivalent of ls on unix.


{-
auto_detect the project type of current folder
by matching the strings in ~/.p/packages/<language>/match.regex
-}
auto_detect :: String -> [String] -> IO String
auto_detect args_language [] = do
  return args_language


auto_detect args_language (language:languages) = do
  output <- call $ ls_command -- Get Direcotry structure
  
  let language_path = create_path [p_folder,"packages",language,"match.regex"]

  match_regex_handle <- openFile language_path ReadMode
  match_regex <- hGetContents match_regex_handle

  if output =~ match_regex
        then return language
        else (auto_detect args_language languages)

-- Create Path from parts/ folders / file names.
create_path :: [String] -> String
create_path parts = (intercalate [pathSeparator] parts)

-- Match a substring in another string
substring :: String -> String -> Bool
substring (x:xs) [] = False
substring xs ys
  | prefix xs ys = True
  | substring xs (tail ys) = True
  | otherwise = False

-- Match for the prefix of two strings to be equal
-- Assume that there are infinitly many [] before
-- a strings beginning.
prefix :: String -> String -> Bool
prefix [] ys = True
prefix (x:xs) [] = False
prefix (x:xs) (y:ys) = (x == y) && prefix xs ys
