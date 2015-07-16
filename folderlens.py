import os
import sys
def makelinks(dest_root, source_root):
	for current_path, dirs, files in os.walk(source_root):
		for file in files:
			source_path = os.path.join(current_path, file)

			relative_path = os.path.relpath(source_path, source_root)
			dest_path = os.path.join(dest_root, relative_path)

			#ensure directory for symlink exists
			os.makedirs(os.path.dirname(dest_path), exist_ok=True)
			#create symlink
			os.symlink(source_path, dest_path)

def main(argv):
	#stop with the indexes
	makelinks(argv[2],argv[1])

if __name__ == "__main__":
	main(sys.argv)