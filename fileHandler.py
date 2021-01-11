import os

boost_location = "C:/Users/Admin/Desktop/"

class FileHandler:
	@staticmethod
	def getSubFolders(path):
		tmp = [f.path for f in os.scandir(path) if f.is_dir()]
		rv = []
		#for i in tmp: rv.append(FileHandler.formatPath(i))
		for i in tmp: rv.append(i)
		return rv

	@staticmethod
	def getSubFiles(path):
		tmp = [f.path for f in os.scandir(path) if f.is_file()]
		rv = []
		#for i in tmp: rv.append(FileHandler.formatPath(i))
		for i in tmp: rv.append(i)
		return rv

	@staticmethod
	def formatPath(path):
		return path.replace("\\", "/").replace(boost_location, "")

	@staticmethod
	def pathToRelative(path):
		# "C:\Users\Admin\Desktop\boost\function_types\components.hpp"
		path = FileHandler.formatPath(path)
		return path

	@staticmethod
	def include(path, step):
		return ("#include \"" + "../"*step + FileHandler.pathToRelative(path) + "\"")

	@staticmethod
	def editFiles(path, step, verbose = False):
		slash = "../"*step
		used = []
		for file in FileHandler.getSubFiles(path):
			file = file.replace('\\', '/')
			isModified = False
			if verbose: print (f"Doing {file}... ", end="")
			outContent = ""
			with open(file, encoding='utf-8') as file_in:
				for line in file_in:
					if "BOOST_PP_ITERATE" in line:
						if file not in used:
							print(file)
							used.append(file)
					line = line.strip()
					if line == "":
						continue # will completely remove all blank lines to save space since you'd not want to read these source files.
					
					#some includes are formated as "#   include" for some reason. So the following code deals with that.
					try: 
						if line[1] == "#": 
							line = "#" + line[1:].strip()
							isModified = True
					except IndexError: pass

					for i in range(1, 6+1):
						char = "#" + " " * i
						if char in line:
							line = line.replace(char, "#")
							isModified = True
					line = line.replace("#   define BOOST_COMPILER_CONFIG", "#define BOOST_COMPILER_CONFIG")

					if "#include <boost/" in line:
						if "//" in line:
							line = line.split('//')[0]#.strip()# we will strip down below
						line = ("#" + line[1:].strip()).replace("#include <boost/", f"#include \"{slash}boost/")[:-1] + '"'
						isModified = True
					if "#define BOOST_USER_CONFIG <boost/" in line:
						#define BOOST_USER_CONFIG <boost/
						line = ("#" + line[1:].strip()).replace(
							"#define BOOST_USER_CONFIG <boost/", f"#define BOOST_USER_CONFIG \"{slash}boost/")[:-1] + '"'
						isModified = True
					# #   define BOOST_COMPILER_CONFIG "boost/config/compiler/gcc_xml.hpp"
					if "#define BOOST_COMPILER_CONFIG <boost/" in line:
						#define BOOST_USER_CONFIG <boost/
						line = ("#" + line[1:].strip()).replace(
							"#define BOOST_COMPILER_CONFIG <boost/", f"#define BOOST_COMPILER_CONFIG \"{slash}boost/")[:-1] + '"'
						print("Deed is done.")
						isModified = True
					outContent += line + "\n"

			if isModified:
				f = open(file, "w", encoding='utf-8')
				f.write(outContent)
				f.close()
				if verbose: print("Done!")
			else:
				if verbose: print("Unmodified!")

	@staticmethod
	def run(path, step):
		for i in FileHandler.getSubFolders(path):
			if not i == []:
				FileHandler.run(i, step+1)
		FileHandler.editFiles(path, step) # even if there are now sub folder then still run

if __name__ == "__main__":
	steps = 1
	startDir = boost_location + "boost"
	#print(FileHandler.include("C:\\Users\\Admin\\Desktop\\boost\\function_types\\components.hpp", steps+1))
	#for i in FileHandler.getSubFolders(startDir):
	#	if not i == []:
	#		print(i)
	#for i in FileHandler.getSubFiles(startDir):
	#	print(i)"""
	FileHandler.run(startDir, steps)
	#FileHandler.run(startDir, steps) # run again just to make sure.