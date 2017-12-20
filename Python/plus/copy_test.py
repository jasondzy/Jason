
from multiprocessing import Pool
import os
import shutil

def copy_files(name):
	
	print('-----%s--------'%name)
	fr = open('test/'+name)
	fw = open('test_bak/'+name,'w')

	content = fr.read()
	fw.write(content)

	fr.close()
	fw.close()





def main():

	if not os.path.exists('test_bak/'):
		os.mkdir('test_bak')
	else:
		shutil.rmtree('test_bak')
		os.mkdir('test_bak')
	source_files = os.listdir('test')

	pool = Pool(5)

	for name in source_files:
		pool.apply_async(copy_files,(name,))

	pool.close()
	pool.join()


if __name__ == '__main__':
	main()