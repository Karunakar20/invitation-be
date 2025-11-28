import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.initializer.category.category import CategoryInitializer


def main():
      CategoryInitializer().categotyInitializer()
      CategoryInitializer().subCategotyInitializer()


if __name__ == "__main__":
      main()