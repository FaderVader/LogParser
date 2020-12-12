import sys, os, pathlib
proj_dir = str(pathlib.Path((pathlib.Path(__file__).parent)).parent)
src_dir = os.path.join(proj_dir, 'src')
sys.path.append(src_dir) 
