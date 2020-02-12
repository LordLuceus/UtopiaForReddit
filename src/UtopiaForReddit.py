import slave

if __name__ == "__main__":
	import cProfile
	cProfile.run("slave._real_main()", None, "cumulative")
