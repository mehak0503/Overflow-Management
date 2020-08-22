# INTRODUCTION
<pre>
A process that checks a directory that fills up with files every minute(parameter)
If it is over a set parameter(20,000)
   The program will look at the age of files
      and move (To a series of overflow directories until it is back under 20K.
          Take the newst 5K(parameter) files dropping the original DIR to 15K files.
             make sure the newest files are closed or completed. On NFS MOUNT.
                 Might need a wait a few minutes to see if the file is completed?(wait time parameter)
          MOVE TO DIR needs a #(number in the name Ending) to allow several to fill to 20K each.
IF the OVERFLOW DIR is over the 15K
   Create another DIR from the Original Name Plus a Number (Max 9) i.e /data/input/FILES
       /data/input/FILES1   and  ......  /data/input/FILES9
If the Original DIR is full over the 20K, SEND EMAIL  admin (parameter) explaining "Queue FULL".
Also an option to run a program after sending mail. To start the extra processioning for the other directories. (Might be a restful API call)
....
Back to testing Interval of the original DIR.
If overfull and there are still files in the Numbered Overflow DIRs, Move to the next one.
  example - Queue was full and the there was already files moved to FILES1(15,000) and FILES2(5,000).  FILES3 dir is empty - use it, send Email and possible RESTFUL call.
</pre>
