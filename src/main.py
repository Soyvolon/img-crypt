# Last Edit: 2022-10-28
# Author(s): Bounds

# This file initializes the startup class for the application to run.
# it will only execute if this module as a whole is executed.

def main():
    from startup import Startup
    runner = Startup()
    runner.initialize()

if __name__ == "__main__":
    main()