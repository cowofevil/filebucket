#!/usr/bin/env python
'''
.. module:: filebucketapp
   :platform: Linux, Windows
   :synopsis: Create files on demand using patterns.
   :license: BSD, see LICENSE for more details.

.. moduleauthor:: Ryan Gard <ryan.a.gard@outlook.com>
'''
__version__ = 1.1

#===================================================================================================
# Imports
#===================================================================================================
import sys
import os.path
import optparse
import random

#===================================================================================================
# Globals
#===================================================================================================
#The file name to use to create the big file.
strFile = ""

#The seed to use to create the big file from
strSeed = ""

#The size of the file in megabytes
intSize = 0

#Object parser
objArgParser = None

#Options object for holding the command line arguments
objOptions = None
objArgs = None

#===================================================================================================
# Functions
#===================================================================================================
def RandomNames(prefix, suffix, count):
    '''Create an array of random generated strings that are 15 characters in length.
        
    Args:
        prefix (str): The string to use to prefix the names.
        count (int): The number of random strings.
    
    Returns:
        ([str]): Array of strings.
    
    Raises:
        RuntimeError: Anything goes wrong.
    '''
    
    #The array of strings to return
    arrRandomStrings = []
    
    #The possible characters to use in the randomly generated
    #string.
    arrCharset = [chr(x) for x in range(97, 123)] + [str(x) for x in range(10)]
    
    #Seed the random number generator
    random.seed()
    
    #Create the strings
    for i in range(count):  # @UnusedVariable
        strRandomChars = ''
        strTemp = ''
        
        #Loop until we generate a good string
        while 1:
            #Create a 15 character suffix
            for k in range(15):  # @UnusedVariable
                strRandomChars += random.choice(arrCharset)
            
            #Create a temp string
            strTemp = str(prefix) + str(strRandomChars) + str(suffix)
            
            #Check to make sure the string is unique
            if strTemp in arrRandomStrings:
                #try again
                continue
            else:
                #Add the new string to the array of strings.
                arrRandomStrings.append(strTemp)
                break
        
    #return the array of strings created
    return arrRandomStrings
        
def CreateFile(filename, seed, size):
    '''Create an array of random generated strings that are 15 characters in length.
        
    Args:
        filename (str): The target name of the file.
        seed (str): The file to use as the seed.
        size (int): The size in megabytes of the target file.
    
    Returns:
        None.
    
    Raises:
        RuntimeError: Anything goes wrong.
    '''
    
    #Seed file handle
    SEEDFILE = None
    
    #Target file handle
    TARGETFILE = None
    
    #Number of cycles needed to make the file
    intCycles = 0  # @UnusedVariable
    
    #The seed file buffer
    strSeedFileBuffer = ""

    #Validate the size parameter and makes sure it is not negative
    if size < 1:
        raise RuntimeError("Size parameter is out of range! (Must be bigger than zero!)")
        return

    #Verify that the seed file exists and the size is 128KB
    if not os.path.exists(seed):
        raise RuntimeError("The seed file does not exist!")
    elif os.path.getsize(seed) != 131072:
        raise RuntimeError("Seed file is not 128KB!")
    
    #Open the seed file and load the file into memory
    try:
        SEEDFILE = open(seed, 'rb', 131072)
        strSeedFileBuffer = SEEDFILE.read()
    except IOError:
        raise RuntimeError("Can't read the seed file!")
    finally:
        SEEDFILE.close()

    #Open the target file handle in write mode
    try:
        TARGETFILE = open(filename, 'wb', 131072)
    except IOError:
        raise RuntimeError("Can't open the target file!")
        TARGETFILE.close()
    
    #Calculate the number of cycles needed to write the file
    intCycles = int((size * 1048576) / 131072)
    
    #Write the information to the file
    try:
        for i in range(intCycles):  # @UnusedVariable
            TARGETFILE.write(strSeedFileBuffer)
    except IOError:
        raise RuntimeError("Can't write to the target file.")
    
    #Close the file and exit
    TARGETFILE.close()
    return

def Create1KBFile(filename):
    '''Create a 1KB sized file.
        
    Args:
        filename (str): The target name of the file.
    
    Returns:
        None.
    
    Raises:
        RuntimeError: Anything goes wrong.
    '''
    
    #Target file handle
    TARGETFILE = None
    
    #The buffer to write to the file.
    bytBuffer = "\xff" * 1024

    #Open the target file handle in write mode
    try:
        TARGETFILE = open(filename, 'wb', 1024)
    except IOError:
        raise RuntimeError("Can't open the target file!")
        TARGETFILE.close()
    
    #Write the information to the file
    try:
        TARGETFILE.write(bytBuffer)
    except IOError:
        raise RuntimeError("Can't write to the target file.")
    
    #Close the file and exit
    TARGETFILE.close()
    return

#===================================================================================================
# Main
#===================================================================================================
def main():
    #Create a args parser
    objArgParser = optparse.OptionParser(usage="filebucket [-d] [-s] [-f] [-p] [-u] [-c]", version="filebucket " + str(__version__))
    objArgParser.add_option("-d", "--seed", dest="seed", type="string",
                  help="the seed file from which the target file is created (required)", metavar="SEED")
    objArgParser.add_option("-s", "--size", dest="size", type="int",
                  help="the size of the target file in megabytes (required)", metavar="SIZE")
    objArgParser.add_option("-f", "--file", dest="file", type="string",
                  help="the target file path and name (can only be specified when NOT using the count option)", metavar="FILE")
    objArgParser.add_option("-p", "--prefix", dest="prefix", type="string",
                  help="the prefix to add to the random file name which can include a path (can only be used with the count option)", metavar="PREFIX")
    objArgParser.add_option("-u", "--suffix", dest="suffix", type="string",
                  help="the suffix to add to the random file name (can only be used with the count option)", metavar="SUFFIX")
    objArgParser.add_option("-c", "--count", dest="count", type="int",
                  help="the number of files to write (optional)", metavar="COUNT")
    objArgParser.add_option("-k", "--kilobyte", dest="kb", action="store_true",
                  help="create files that are 1KB in size (cannot be used in conjuction with the --size or --seed options)")
    objArgParser.set_defaults(seed="")
    objArgParser.set_defaults(size=0)
    objArgParser.set_defaults(file="")
    objArgParser.set_defaults(count=False)
    objArgParser.set_defaults(prefix="")
    objArgParser.set_defaults(suffix="")
    objArgParser.set_defaults(kb=False)
    
    #Parse the arguments
    (objOptions, objArgs) = objArgParser.parse_args()  # @UnusedVariable

    #Check to make sure the user supplied all the required arguments.
    if objOptions.file != "" and objOptions.count is not False:
        print("You can only specify a file name if you specify the count option!")
        sys.exit(1)
    elif objOptions.count is False and (objOptions.prefix != "" or objOptions.suffix != ""):
        print("Prefix and suffix can only be used with the count option!")
        sys.exit(1)
    elif objOptions.count is not False and objOptions.count < 1:
        print("Count must be larger than 0!")
        sys.exit(1)
    elif objOptions.seed == "" and objOptions.kb == False:
        print("Command line error: no seed file specified!")
        sys.exit(1)
    elif objOptions.size == 0 and objOptions.kb == False:
        print("Command line error: size not specified or size set to zero!")
        sys.exit(1)
    elif objOptions.seed != "" and objOptions.kb == True:
        print("Command line error: seed cannot be specified along with the 1KB option!")
        sys.exit(1)
    elif objOptions.size != 0 and objOptions.kb == True:
        print("Command line error: size cannot be specified along with the 1KB option!")
        sys.exit(1)
        
    #Attempt to write the file.
    try:
        if objOptions.count is not False:
            #Create an array of names
            arrFileNames = RandomNames(objOptions.prefix, objOptions.suffix, objOptions.count)
            for i in range(objOptions.count):
                if objOptions.kb:
                    Create1KBFile(arrFileNames[i])
                else:
                    CreateFile(arrFileNames[i], objOptions.seed, objOptions.size)
        elif objOptions.count is False and objOptions.file != "":
            if objOptions.kb:
                Create1KBFile(objOptions.file)
            else:
                CreateFile(objOptions.file, objOptions.seed, objOptions.size)
        elif objOptions.count is False and objOptions.file == "":
            if objOptions.kb:
                Create1KBFile(RandomNames('', '', 1)[0])
            else:
                CreateFile(RandomNames('', '', 1)[0], objOptions.seed, objOptions.size)
    except RuntimeError, ex:
        print(("Error: " + ex[0]))
        sys.exit(1)
        
    #Exit the program nicely.
    sys.exit(0)

if __name__ == "__main__":
    main()
