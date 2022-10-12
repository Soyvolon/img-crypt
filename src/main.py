# This file initalizes the startup class for the application to run.
# it will only execute if this module as a whole is executed.

def main():
    from startup import Startup
    runner = Startup()
    runner.initalize()

if __name__ == "__main__":
    main()