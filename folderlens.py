import os
import sys

def get_mappings(dest_root, source_root):
	link_mapping = {} # dest, source mapping
	for current_path, dirs, files in os.walk(source_root):
		for file in files:
			source_path = os.path.join(current_path, file)

			relative_path = os.path.relpath(source_path, source_root)
			dest_path = os.path.join(dest_root, relative_path)

			link_mapping[dest_path] = source_path
	return link_mapping

def merge_mappings(dict_list):
	merged = {}
	duplicates = {}
	for dict in dict_list:
		for dest, source in dict.items():
			if dest in duplicates:
				duplicates[dest].append(source)
			else:
				if dest in merged:
					duplicates[dest] = [merged.pop(dest), source]
				else:
					merged[dest] = source
	return merged, duplicates

def write_symlinks(dict):
	for dest_path, source_path in dict.items():
		#ensure directory for symlink exists
		os.makedirs(os.path.dirname(dest_path), exist_ok=True)
		#create symlink
		os.symlink(source_path, dest_path)

def main(argv):
	out_dir = argv[1]
	in_dirs = [argv[2], argv[3]]

	#stop with the indexes eventually
	mappings = [get_mappings(out_dir, path) for path in in_dirs]
	merged, duplicates = merge_mappings(mappings)

	if len(duplicates) > 0:
		print("Conflicts found")
		print(duplicates)
		
	write_symlinks(merged)

if __name__ == "__main__":
	main(sys.argv)