module Project
    (
     auto_detect
     ) where

import Call (call)
import Config (LS_COMMAND) -- Command equivalent of ls on unix.

{-
auto_detect the project type of current folder
by matching the strings in ~/.p/<language>/match.txt
-}
auto_detect :: String -> IO String
auto_detect args_language = do
  output <- call $ LS_COMMAND -- Get Direcotry structure


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
