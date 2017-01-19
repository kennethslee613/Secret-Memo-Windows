import os.path, ctypes, hashlib, uuid, random, string

#sets dir to the location of the .exec
#exec_path = os.path.dirname(os.path.realpath(__file__))
exec_path = "C:\\Users\\" + os.getlogin() + r"\AppData\Roaming"
folder_path = exec_path + "\Memopad"
pw_path = folder_path + "\Password.txt"

if "Memopad" not in os.listdir(exec_path):
	os.mkdir(folder_path)
	ctypes.windll.kernel32.SetFileAttributesW(folder_path, 2)

os.chdir(folder_path)
rand = uuid.uuid4().hex

#checks to see if password exists and creates one if it doesn't
if "Password.txt" not in os.listdir(folder_path):
	if os.listdir(folder_path) == []:
		temppw = "1234"
		pwhash = hashlib.sha512(temppw.encode()).hexdigest() + "o" + rand
		pw = open("Password.txt", "w+")
		pw.write(pwhash)
		pw.close()
		ctypes.windll.kernel32.SetFileAttributesW(pw_path, 2)
	else:
		for i in os.listdir(folder_path):
			os.remove(i)
		temppw = "1234"
		pwhash = hashlib.sha512(temppw.encode()).hexdigest() + "o" + rand
		pw = open("Password.txt", "w+")
		pw.write(pwhash)
		pw.close()
		ctypes.windll.kernel32.SetFileAttributesW(pw_path, 2)
		print("No password detected. All memos will be deleted.")

def check_password(pw, inputpw):
	pw, rand = pw.split("o")
	if pw == hashlib.sha512(inputpw.encode()).hexdigest():
		return True
	else:
		return False

def encode2(string):
	S = ""
	for i in string:
		i = str((int(i) + 2) % 10)
		S += i
	return S

def decode2(string):
	S = ""
	for i in string:
		i = str((int(i) - 2) % 10)
		S += i
	return S

def encode(memo):
	m = ""
	for i in memo:
		m += encode2(str(ord(i))) + random.choice(string.ascii_lowercase[:6])
	return m

def decode(m):
	if m == "":
		return ""
	else:
		count = 0
		while m[count] not in "abcdef":
			count += 1
		return chr(int(decode2(m[:count]))) + decode(m[(count + 1):])

end = False
while not end:
	password = input("Memopad! Please eneter the password. Type 'quit' to exit (original password is 1234): ")
	with open(pw_path, "r") as pwtxt:
		currentpw = pwtxt.read()
	if check_password(currentpw, password):
		correctpw = True
		while correctpw:
			print("List of commands:")
			print("    add                      add a line of text to a memo")
			print("    delete                   delete a line of text or a memo")
			print("    read                     read the content of a memo")
			print("    create                   create a new memo")
			print("    changepassword           change password")
			print("    quit                     exit the program")
			q1 = input("What would you like to do? ")
			if q1 == "add":
				if os.listdir(folder_path) == ["Password.txt"]:
					print("There are no memos.")
					print("----------------------------")
				else:
					print("Here is a list of memos:")
					for i in os.listdir(folder_path):
						if i != "Password.txt":
							print("    " + i[:-4])
					q2 = input("Which memo would you like to add a line to? ")
					if q2 + ".txt" not in os.listdir(folder_path):
						print("That memo does not exist.")
						print("----------------------------")
					else:
						print(q2 + ": ")
						with open(q2 + ".txt") as readmemo:
							lines = readmemo.readlines()
							count = 0
							for line in lines:
								if count < len(lines) - 1:
									print("    " + str(count + 1) + ". " + decode(line[:-1]))
								else:
									print("    " + str(count + 1) + ". " + decode(line))
								count += 1
						q3 = input("After which line would you like to add (0 to add as first line)? ")
						if q3.isdigit() and int(q3) in range(count + 1):
							q4 = input("Enter the line of text to add: ")
							lines.insert(int(q3), encode(q4))
							for i in range(len(lines)):
								if i < len(lines) - 1:
									if lines[i][-1] != "\n":
										lines[i] = lines[i] + "\n"
							ctypes.windll.kernel32.SetFileAttributesW(folder_path + "\\" + q2 + ".txt", 0)
							memo = open(q2 + ".txt", "w+")
							memo.writelines(lines)
							memo.close()
							ctypes.windll.kernel32.SetFileAttributesW(folder_path + "\\" + q2 + ".txt", 2)
							print("----------------------------")
						else:
							print("That line does not exist.")
							print("----------------------------")
			elif q1 == "delete":
				q2 = input("Would you like to delete a memo or a line of a memo (memo or line)? ")
				if q2 == "memo":
					print("Here is a list of memos:")
					for i in os.listdir(folder_path):
						if i != "Password.txt":
							print("    " + i[:-4])
					q3 = input("Which memo would you like to delete? ")
					if q3 + ".txt" not in os.listdir(folder_path):
						print("That memo does not exist.")
						print("----------------------------")
					else:
						os.remove(q3 + ".txt")
						print(q3 + " has been deleted.")
						print("----------------------------")
				elif q2 == "line":
					print("Here is a list of memos:")
					for i in os.listdir(folder_path):
						if i != "Password.txt":
							print("    " + i[:-4])
					q3 = input("Which memo would you like to delete a line from? ")
					if q3 + ".txt" not in os.listdir(folder_path):
						print("That memo does not exist.")
						print("----------------------------")
					else:
						print(q3 + ": ")
						with open(q3 + ".txt") as readmemo:
							lines = readmemo.readlines()
							count = 0
							for line in lines:
								if count < len(lines) - 1:
									print("    " + str(count + 1) + ". " + decode(line[:-1]))
								else:
									print("    " + str(count + 1) + ". " + decode(line))
								count += 1
						q4 = input("Which line would you like to delete? ")
						if q4.isdigit() and int(q4) - 1 in range(count):
							lines = lines[:int(q4) - 1] + lines[int(q4):]
							for i in range(len(lines)):
								if i < len(lines) - 1:
									if lines[i][-1] != "\n":
										lines[i] = lines[i] + "\n"
								elif i == len(lines) - 1 and lines[i][-1] == "\n":
									lines[i] = lines[i][:-1]
							ctypes.windll.kernel32.SetFileAttributesW(folder_path + "\\" + q3 + ".txt", 0)
							memo = open(q3 + ".txt", "w+")
							memo.writelines(lines)
							memo.close()
							ctypes.windll.kernel32.SetFileAttributesW(folder_path + "\\" + q3 + ".txt", 2)
							print("----------------------------")
				else:
					print("Invalid command.")
					("----------------------------")
				#at a certain line or a memo

			elif q1 == "read":
				if os.listdir(folder_path) == ["Password.txt"]:
					print("There are no memos.")
					print("----------------------------")
				else:
					print("Here is a list of memos:")
					for i in os.listdir(folder_path):
						if i != "Password.txt":
							print("    " + i[:-4])
					q2 = input("Which memo would you like to read? ")
					if q2 + ".txt" not in os.listdir(folder_path):
						print("That memo does not exist.")
						print("----------------------------")
					else:
						print(q2 + ": ")
						with open(q2 + ".txt") as readmemo:
							lines = readmemo.readlines()
							count = 0
							for line in lines:
								if count < len(lines) - 1:
									print("    " + decode(line[:-1]))
								else:
									print("    " + decode(line))
								count += 1
						print("----------------------------")
			elif q1 == "create":
				q2 = input("Give the new memo a name: ")
				if q2 + ".txt" in os.listdir(folder_path):
					print("This memo already exists.")
					print("----------------------------")
				else:
					q3 = input("Type your new memo: ")
					newmemo = open(q2 + ".txt", "w+")
					newmemo.write(encode(q3))
					newmemo.close()
					ctypes.windll.kernel32.SetFileAttributesW(folder_path + "\\" + q2 + ".txt", 2)
					print("----------------------------")
			elif q1 == "changepassword":
				q2 = input("Enter your old password: ")
				if check_password(currentpw, q2):
					q3 = input("Enter your new password: ")
					pwhash = hashlib.sha512(q3.encode()).hexdigest() + "o" + rand
					ctypes.windll.kernel32.SetFileAttributesW(pw_path, 0)
					pw = open("Password.txt", "w")
					pw.write(pwhash)
					pw.close()
					ctypes.windll.kernel32.SetFileAttributesW(pw_path, 2)
					correctpw = False
					print("----------------------------")
				elif q2 == "quit":
					correctpw = False
					end = True
				else:
					print("Incorrect password")
					correctpw = False
					print("----------------------------")
			elif q1 == "quit":
				correctpw = False
				end = True
			else:
				print("Invalid command.")
				print("----------------------------")
	elif password == "quit":
		end = True
	else:
		print("Incorrect password.")
		print("----------------------------")