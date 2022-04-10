import pkg_resources

def generate_pip_freeze() -> str:
    requirements = ""
    for dist in pkg_resources.working_set:
        req = dist.as_requirement()
        requirements += f"{req}\n"
    return requirements

if __name__ == "__main__":
    requirements = generate_pip_freeze()
    with open('requirements.txt', 'w')  as a:
        a.write(requirements)