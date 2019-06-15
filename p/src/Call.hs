module Call
    (
     call
     ) where

import System.Process as Process
import System.IO as IO

call :: String -> IO String
call command = do
        (_,Just output_handle,_, _)  <- Process.createProcess ( Process.shell command ) { std_out = Process.CreatePipe }
        IO.hGetContents output_handle