import sys
import subprocess


def get_module_list(main_commit_hash, fork_commit_hash):
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", main_commit_hash, fork_commit_hash],
            stdout=subprocess.PIPE,
        )
    except Exception as e:
        print(e)
        exit(1)
    modules = result.stdout.decode("utf-8").split("\n")
    module_list = [module for module in modules if module.startswith("workflows")]
    module_list = ['/'.join(module.split("/", 4)[:4]) for module in module_list]
    return list(set(module_list))


def test_module(module_path):
    try:
        result = subprocess.run(["bash", ".tests.sh"], cwd=module_path)
    except Exception as e:
        print(e)
        return 1
    return result.returncode


def run_tests(module_list):
    passed_modules = []
    failed_modules = []
    for module in module_list:
        if test_module(module) == 0:
            passed_modules.append(module)
        else:
            failed_modules.append(module)

    print("Passed modules: ", passed_modules)
    if failed_modules:
        print("Failed modules: ", failed_modules)
        exit(1)
    else:
        print("All modules passed.")
        exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script.py <first_argument> <second_argument>")
        sys.exit(1)
    main_commit_hash = sys.argv[1]
    fork_commit_hash = sys.argv[2]
    module_list = get_module_list(main_commit_hash, fork_commit_hash)
    run_tests(module_list)