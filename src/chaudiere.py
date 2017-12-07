# Copyright Paul Dardeau, SwampBits LLC 2014
# BSD License

import socket

# ******************************************************************************
# ******************************************************************************


class Logger:
    '''
    * Logs a critical level message
    * @param msg the message to log
    '''
    @staticmethod
    def critical(msg):
        print "critical: " + msg

    '''
    * Logs an error level message
    * @param msg the message to log
    '''
    @staticmethod
    def error(msg):
        print "error: " + msg

    '''
    * Logs a warning level message
    * @param msg the message to log
    '''
    @staticmethod
    def warning(msg):
        print "warning: " + msg

    '''
    * Logs an info level message
    * @param msg the message to log
    '''
    @staticmethod
    def info(msg):
        print "info: " + msg

    '''
    * Logs a debug level message
    * @param msg the message to log
    '''
    @staticmethod
    def debug(msg):
        print "debug: " + msg

    '''
    * Logs a verbose level message
    * @param msg the message to log
    '''
    @staticmethod
    def verbose(msg):
        print "verbose: " + msg

# ******************************************************************************
# ******************************************************************************


class StrUtils:

    '''
    * Strips leading and trailing whitespace from a string
    * @param stringToStrip the string whose whitespace is to be removed
    * @return the stripped string
    '''
    @staticmethod
    def strip(stringToStrip):
        return stringToStrip.strip()

    '''
    * Strips trailing characters from a string
    * @param stringToStrip string whose trailing characters are to be removed
    * @param stripChar the character to strip from the end of the string
    * @return the stripped string
    '''
    @staticmethod
    def stripTrailing(stringToStrip, stripChar):
        return stringToStrip.rstrip(stripChar)

    '''
    * Pads a string to a specified length with a padding character
    * @param stringToPad the string to be padded
    * @param padChar the padding character
    * @param paddedLength the desired length of the string (with padding)
    * @return string padded to desired length with padding character
    '''
    @staticmethod
    def padRight(stringToPad, padChar, paddedLength):
        return stringToPad.ljust(paddedLength, padChar)

    '''
    * Determines if a string begins with a specified prefix
    * @param haystack the string whose prefix is to be examined
    * @param needle the prefix we're looking for
    * @return boolean indicating whether the prefix exists
    '''
    @staticmethod
    def startsWith(haystack, needle):
        return haystack.startswith(needle)

# ******************************************************************************
# ******************************************************************************


class StringTokenizer:

    '''
    * Constructs new instance using a string with tokens and a delimiter
    * @param tokenString the string with tokens that will be parsed
    * @param delimiter the delimiter that separates the tokens
    '''
    def __init__(self, tokenString, delimiter):
        self.tokenList = tokenString.split(delimiter)
        self.tokenIndex = 0

    '''
    * Retrieves the number of tokens found
    * @return the number of tokens
    '''
    def countTokens(self):
        return len(self.tokenList)

    '''
    * Determines if more tokens are available for retrieval
    * @return boolean indicating if more tokens are available
    '''
    def hasMoreTokens(self):
        return self.tokenIndex < len(self.tokenList)

    '''
    * Retrieves the next token
    * @return the next token
    '''
    def nextToken(self):
        token = self.tokenList[self.tokenIndex]
        self.tokenIndex += 1
        return token

# ******************************************************************************
# ******************************************************************************


class KeyValuePairs:

    '''
    * Constructs a new KeyValuePairs instance
    '''
    def __init__(self):
        self.mapKeyValues = {}

    '''
    * Determines if the specified key exists in the collection
    * @return boolean indicating whether the key exists
    '''
    def hasKey(self, key):
        return key in self.mapKeyValues

    '''
    * Adds a new key/value pair to the collection
    * @param key the key for the new pair
    * @param value the value for the new pair
    '''
    def addPair(self, key, value):
        self.mapKeyValues[key] = value

    '''
    * Removes a pair from the collection
    * @param key the key that identifies the pair
    '''
    def removePair(self, key):
        self.mapKeyValues.remove(key)

    '''
    * Retrieves the value associated with the specified key
    * @param key the key whose value is being retrieved
    * @return the value associated with the key
    '''
    def getValue(self, key):
        return self.mapKeyValues[key]

    '''
    * Removes all key/value pairs in the collection
    '''
    def clear(self):
        self.mapKeyValues = {}

    '''
    * Retrieves the number of pairs stored in the collection
    * @return the number of pairs
    '''
    def size(self):
        return len(self.mapKeyValues)

    '''
    * Determines if there are any pairs stored in the collection
    * @return boolean indicating if the collection is empty
    '''
    def empty(self):
        return 0 == len(self.mapKeyValues)

    '''
    * Retrieves a list of the keys for all pairs stored in the collection
    * @return list of stored keys
    '''
    def getKeys(self):
        keys = []
        for key in self.mapKeyValues.keys():
            keys.append(key)
        return keys

    '''
    * Prints the keys and values. This is primarily a debugging aid.
    '''
    def printKeyValues(self):
        if not self.empty():
            for key in self.getKeys():
                print "key='" + key + "', value='" + self.getValue(key) + "'"
        else:
            print "KeyValuePairs object is empty"

# ******************************************************************************
# ******************************************************************************


class IniReader:

    CLOSE_BRACKET = "]"
    COMMENT_IDENTIFIER = "#"
    EOL_CR = "\r"
    EOL_LF = "\n"
    OPEN_BRACKET = "["

    '''
    * Constructs a new IniReader using the specified file path
    * @param filePath the file path to the INI configuration file
    * @throws Exception
    '''
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileContents = None
        if not self.readFile():
            raise Exception("unable to read configuration file: " + filePath)

    '''
    * Retrieves the identifier for a section within the configuration file
    * @param sectionName the name of the section
    * @return the sectionName surrounded by square brackets
    '''
    @staticmethod
    def bracketedSection(sectionName):
        return IniReader.OPEN_BRACKET + StrUtils.strip(sectionName) + \
               IniReader.CLOSE_BRACKET

    '''
    * Determines if the specified section exists within the configuration file
    * @param sectionName name of the section whose existence is being tested
    * @return boolean indicating whether the section exists
    '''
    def hasSection(self, sectionName):
        sectionId = IniReader.bracketedSection(sectionName)
        return -1 != self.fileContents.find(sectionId)

    '''
    * Reads the configuration file specified on construction
    * @return boolean indicating if the file was successfully read
    '''
    def readFile(self):
        with open(self.filePath, "r") as inputFile:
            self.fileContents = inputFile.read()

        # strip out any comments
        strippingComments = True
        posCurrent = 0

        while strippingComments:
            posCommentStart = \
                self.fileContents.find(IniReader.COMMENT_IDENTIFIER,
                                       posCurrent)
            if -1 == posCommentStart:
                # not found
                strippingComments = False
            else:
                posCR = self.fileContents.find(IniReader.EOL_CR,
                                               posCommentStart+1)
                posLF = self.fileContents.find(IniReader.EOL_LF,
                                               posCommentStart+1)
                haveCR = (-1 != posCR)
                haveLF = (-1 != posLF)

                if not haveCR and not haveLF:
                    # no end-of-line marker remaining
                    # erase from start of comment to end of file
                    self.fileContents = self.fileContents[0:posCommentStart]
                    strippingComments = False
                else:
                    # at least one end-of-line marker was found

                    # were both types found
                    if haveCR and haveLF:
                        posEOL = posCR

                        if posLF < posEOL:
                            posEOL = posLF
                    else:
                        if haveCR:
                            # // CR found
                            posEOL = posCR
                        else:
                            # LF found
                            posEOL = posLF

                    beforeComment = self.fileContents[0:posCommentStart]
                    afterComment = self.fileContents[posEOL:]
                    self.fileContents = beforeComment + afterComment
                    posCurrent = len(beforeComment)

        return True

    '''
    * Retrieves the value for the specified key in the specified section
    * @param section the name of the section whose data is being retrieved
    * @param key the identifier for the configuration data being retrieved
    * @return the value for the requested key, or None on error
    '''
    def getSectionKeyValue(self, section, key):
        map = KeyValuePairs()

        if not self.readSection(self, section, map):
            Logger.warning("IniReader readSection returned false")
            return None

        strippedKey = StrUtils.strip(key)

        if not map.hasKey(strippedKey):
            Logger.debug("map does not contain key '" + key + "'")
            return None

        return map.getValue(key)

    '''
    * Reads the specified section from the configuration and populates the
    * passed KeyValuePairs instance
    * @param sectionName name of section whose configuration values to retrieve
    * @param sectionVals kvp instance to populate with configuration data
    * @return boolean indicating whether configuration data could be retrieved
    * @see KeyValuePairs()
    '''
    def readSection(self, sectionName, sectionVals):
        sectionId = IniReader.bracketedSection(sectionName)
        posSection = self.fileContents.find(sectionId)

        if posSection == -1:
            return False

        posEndSection = posSection + len(sectionId)
        startNextSection = self.fileContents.find(IniReader.OPEN_BRACKET,
                                                  posEndSection)

        # do we have another section?
        if startNextSection != -1:
            # yes, we have another section in the file -- read everything
            # up to the next section
            sectionContents = self.fileContents[posEndSection:startNextSection]
        else:
            # no, this is the last section -- read everything left in
            # the file
            sectionContents = self.fileContents[posEndSection:]

        parsingSectionContents = True
        posEol = 0
        index = 0

        # process each line of the section
        while parsingSectionContents:
            posEol = sectionContents.find(IniReader.EOL_LF, index)
            if posEol == -1:
                parsingSectionContents = False
                continue

            line = sectionContents[index:posEol]
            if len(line) > 0:
                posCR = line.find('\r')
                if posCR != -1:
                    line = line[0:posCR]

                posEqual = line.find('=')

                if (posEqual != -1) and (posEqual < len(line)):
                    key = StrUtils.strip(line[0:posEqual])

                    # if the line is not a comment
                    if not StrUtils.startsWith(key,
                                               IniReader.COMMENT_IDENTIFIER):
                        sectionVals.addPair(key,
                                            StrUtils.strip(line[posEqual+1:]))

            index = posEol + 1

        return True

# ******************************************************************************
# ******************************************************************************


class ServiceInfo:

    '''
    * Constructs a new instance of ServiceInfo using name, host, and port
    * @param serviceName the name of the service
    * @param host the host that provides the service
    * @param port the port number that the service is listening on
    '''
    def __init__(self, serviceName=None, host=None, port=0):
        self.serviceName = serviceName
        self.host = host
        self.port = port

    '''
    * Retrieves the name of the service
    * @return the service name
    '''
    def getServiceName(self):
        return self.serviceName

    '''
    * Retrieves the host for the service
    * @return the host
    '''
    def getHost(self):
        return self.host

    '''
    * Retrieves the port number for the service
    * @return the port number
    '''
    def getPort(self):
        return self.port

    '''
    * Sets the name for the service
    * @param serviceName the new name for the service
    '''
    def setServiceName(self, serviceName):
        self.serviceName = serviceName

    '''
    * Sets the host for the service
    * @param host the new host for the service
    '''
    def setHost(self, host):
        self.host = host

    '''
    * Sets the port number for the service
    * @param port the new port value for the service
    '''
    def setPort(self, port):
        self.port = port

# ******************************************************************************
# ******************************************************************************


class Socket:

    '''
    * Constructs a new Socket instance using a host and port
    * @param host the host to connect to
    * @param port the port number that the server is listening on
    '''
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    '''
    * Retrieves the host associated with the socket connection
    * @return the host associated with the socket
    '''
    def getHost(self):
        return self.host

    '''
    * Retrieves the port number associated with the socket
    * @return the port number
    '''
    def getPort(self):
        return self.port

    '''
    * Determines if a socket connection currently exists
    * @return boolean indicating if there is currently a connected socket
    '''
    def isOpen(self):
        return self.socket is not None

    '''
    * Closes the socket connection if one exists
    '''
    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    '''
    * Writes data to the socket
    * @param data the data to write to the socket
    * @return boolean indicating if the data was successfully sent
    '''
    def write(self, data):
        if self.socket is not None:
            if self.socket.sendall(data) is None:
                return 1
            else:
                return 0
        else:
            return 0

    '''
    * Reads the specified number of bytes from the socket connection
    * @param numBytesToRead the number of bytes to read
    * @return the data read from the socket as a string, or None on error
    '''
    def readSocket(self, numBytesToRead):
        if self.socket is not None:
            return self.socket.recv(numBytesToRead)
        else:
            return None

# ******************************************************************************
# ******************************************************************************
