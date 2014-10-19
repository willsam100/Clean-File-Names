#!/usr/bin/python -tt

import sys
import os
import re

extras = ''

######################################
def split(filename):
  (root, ext) = os.path.splitext(filename)
  basename = os.path.basename(root)

  baseWords = remove_data(basename)
  baseWords = create_new_name(baseWords)
  basename = ' '.join(baseWords)
  
  basename += ext
  newName = os.path.join(os.path.dirname(root), basename)
  return newName

######################################

def remove_data(basename):
  #print basename

  basename = re.sub(r'www\.\S+\.\w+', '', basename, re.I)
  baseWords = []
  
  #loop over to find brackets etc, thsi should be a switch
  count = 0
  for i in range(len(basename)):
    if basename[i] == '.':
      baseWords.append(basename[count:i])
      count = i+1
    elif basename[i] == ' ':
      baseWords.append(basename[count:i])
      count = i+1
    elif basename[i] == '-':
      baseWords.append(basename[count:i])
      count = i+1
    elif basename[i] == '{':
      baseWords.append(basename[count:i] )
      count = i
    elif basename[i] == '}':
      baseWords.append(basename[count:i])
      count = i+1
    elif basename[i] == '[':
      baseWords.append(basename[count:i])
      count = i
    elif basename[i] == ']':
      baseWords.append(basename[count:i])
      count = i+1
    elif basename[i] == '(':
      baseWords.append(basename[count:i])
      count = i
    elif basename[i] == ')':
      baseWords.append(basename[count:i])
      count = i+1
    elif basename[i] == '+':
      baseWords.append(basename[count:i])
      count = i+1
    elif basename[i] == '_':
      baseWords.append(basename[count:i])
      count = i+1
  baseWords.append(basename[count:])

  return baseWords

######################################

def create_new_name(baseWords):
  
  newBase = []
  foundYear = ''
  season = ''
  episode = ''
  tvShowInsertPos = ''
  for wd in baseWords:
    if len(wd) > 0: 
      if wd[0] == ' ':
        if len(wd) > 1:
          wd = wd[1:]
      series = re.search(r'[S|s|x]*(\d\d)[E|e|x]*(\d\d)', wd)
      if series:
        notSeries = re.search(r'\d\d\d\d', wd)
        if notSeries:
          newBase.append(notSeries.group(0))
          continue
        season = series.group(1)
        episode = series.group(2)
        tvShowInsertPos = len(newBase)
        continue
      if wd[0] == '(' or wd[0] == '{' or wd[0] == '[' or wd[0] == '-':
        bracketYear = re.match(r'\(|\{|\[[1,2][9,0]\d\d', wd)
        if bracketYear:
        #found a year in brackets removing rest of file name
          break
        wd = ''
    match = re.search(r'720p|DIMENSION|x264|hdtv|divx|torrent|ac3|www|fqm|sitv|xvid|dvd|dvdrip', wd, re.I)
    if match:
      continue
    year = re.match(r'[1,2][9,0]\d\d', wd)
    if year:
      #foundYear = year.group(0)
      continue
    wd = wd.capitalize()    
    if wd != '':
      newBase.append(wd)

  if season:
    show = 'S' + season + 'e' + episode
    newBase.insert(tvShowInsertPos, show)
  if foundYear:
    newBase.append(foundYear)

  return newBase

#######################################
def process_dir(dir):
  files = os.listdir(dir)
  completed = []
  for file in files:
    if file[0] == '.':
      continue
    orignal = os.path.abspath(os.path.join(dir, file))
    if not os.path.isdir(orignal):
      result = split(orignal)
    else:
      basename = os.path.basename(orignal)
      results = remove_data(basename)
      results = create_new_name(results)
      result = ' '.join(results)
      result = os.path.abspath(os.path.join(dir, result))
    tuple = (orignal, result)
    completed.append(tuple)
  return completed

###########################################
def main():
  args = []
  rename = ''
  isFile = '' 
  renameDir = ''
  
  #Check the arguments the user has supplied 

  #If the user did not supply a file/dir then assume the files in the current dir
  if len(sys.argv) == 1:
    args.append(os.getcwd())
  else:
  #check the flags the user has supplied 
    if sys.argv[1] == '-y':
      rename = 'true'
      if len(sys.argv) == 2:
        args.append(os.getcwd())
      if len(sys.argv) >= 3:
        if sys.argv[2] == '-d':
          renameDir = 'true'
          for l in range(3, len(sys.argv)):
            args.append(sys.argv[l])
        else:
          for l in range(2, len(sys.argv)):
            args.append(sys.argv[l])  
      else:
        args.append(os.getcwd())
    elif sys.argv[1] == '-h':
      print 'Usage: ./fixFileName.py dir\n'
      print 'Options:'  
      print '   -y  Confirm the rename'
      print '   -h  Display this menu'
      print '     -d  rename the directory itself'
    #rename the directory itself, not the files inside it
    elif sys.argv[1] == '-d':
      renameDir = 'true'
      if len(sys.argv) >= 3:
        if sys.argv[2] == '-y':
          rename = 'true'
          for l in range(3, len(sys.argv)):
            args.append(sys.argv[l])
        else:
          for l in range(2, len(sys.argv)):
            args.append(sys.argv[l])
      #if the user specificed only -d then give error as this is ambigous what the user desires to do
      else:
        print 'Usage: ./fixFileName.py dir\n'
        print 'Options:'  
        print '   -y  Confirm the rename'
        print '   -h  Display this menu'
        print '     -d  rename the directory itself'
    else:
    #no flags so add all the items
     for l in range(1, len(sys.argv)):
       args.append(sys.argv[l])

  #loop over the items and process them according the flags set
  for arg in args:
    exists = os.path.exists(arg)
    if not exists:
      print 'File does not exist or can\'t be found: ', arg
      continue
    isFile = os.path.isfile(arg)
    if renameDir:
      isFile = 'true'
    if isFile:
      
      #calling function that does the 'heavy lifting'
      (root, ext) = os.path.splitext(arg)
      basename = os.path.basename(root)
      baseWords = remove_data(basename)
      baseWords = create_new_name(baseWords)
      basename = ' '.join(baseWords)
      basename += ext
      file = os.path.join(os.path.dirname(root), basename)
      
      if rename:
        if len(arg) >= len(file):
          if os.path.isfile(file):
            print 'Renaming file', os.path.basename(file)
          else:
            print 'Renaming folder', os.path.basename(file)
            try:      
              os.rename(arg, file)
            except:
              addNumber = 1
              file 
              while os.path.exists((file + ' ' + str(addNumber))):
                addNumber += 1
              os.rename(arg, (file + ' ' + str(addNumber)))
      else:
        print os.path.basename(file)
    else:
      dirs =  process_dir(arg)
      if rename:
        print 'Renaming contents of folder: ', os.path.basename(arg)
        for dir in sorted(dirs):
           if len(dir[1]) > len(arg):
             os.rename(dir[0], dir[1])
             print "%s % 70s" %(str(os.path.basename(dir[0])), ' <= \t ' + str(os.path.basename(dir[1])))
           else:
             print 'Error with file', dir[0]
      else:
        for dir in sorted(dirs):
          print os.path.basename(dir[1])

  return

if __name__ == '__main__':
  print 'jonathan is gay'
  main()
