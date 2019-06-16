module Project
    (
     auto_detect
     ) where

-- stdlib Modules
import Text.Regex.Posix
import System.IO
-- p Modules
import Call (call)
import Config (ls_command,p_folder) -- ls_command: equivalent of ls on unix.


{-
auto_detect the project type of current folder
by matching the strings in ~/.p/packages/<language>/match.regex
-}
auto_detect :: String -> String -> IO String
auto_detect args_language [] = do
  return args_language

auto_detect args_language (language:languages) = do
  output <- call $ ls_command -- Get Direcotry structure
  let language_path = join pathSeparator [p_folder,"packages",language,"match.regex"] 
  match_regex <- hGetContents $ openFile language_path ReadMode
  project_type <- if output ~= match_regex
        then return language
        else (auto_detect args_language languages)
  return project_type

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
