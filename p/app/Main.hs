module Main where

import Call (call)

main :: IO ()
main = do
  -- p Commands:
  -- Every p Command follows this scheme:
  -- p <language> <command>
  -- The <language> part should be omitted, if p can auto detect
  -- the directory structure
  --
