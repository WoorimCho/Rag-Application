# from app.aims import AGENT_CONFIG
from . import AGENT_CONFIG
from app.aims.api.embedding.embedding_handler_local import EmbeddingHandlerLocal


def usage():
    print("Usage: python ai_agent.py [options]")
    print("Options:")
    print("  --help                      Show this help message and exit")
    print("  --version                   Show the version of the AI Agent")
    print("  --config=<file>             Specify a configuration file")
    print("  --load=<file | directory>   Specify a file or directory to load")
    print("  --verbose                   Enable verbose output")
    print("  --run                       Run the AI Agent")

def loadData(file_or_directory=None):
    print(f"Loading data from: {file_or_directory}")
    embedding_handeler = EmbeddingHandlerLocal(file_or_directory)
    embedding_handeler.run()
    # raise NotImplementedError


def main():    
    #print("Script name:", sys.argv[0])
    #print("Arguments:", sys.argv[1:])
    if len(sys.argv) < 2:
        usage()
        return

    for arg in sys.argv[1:]:
        if arg == '--help':
            usage()
            return
        elif arg == '--version':
            print(f"AI Agent Version {AGENT_CONFIG.version}")
            return
        elif arg.startswith('--config='):
            config_file = arg.split('=')[1]
            print(f"Using configuration file: {config_file}")
        elif arg.startswith('--load='):
            file_or_directory = arg.split('=')[1]
            loadData(file_or_directory=file_or_directory)
        elif arg == '--run':
            print("Running AI Agent...")
        else:
            print(f"Unknown option: {arg}")
            usage()
            return

    # Here you would add the logic to run the AI Agent based on the provided options.
    print("AI Agent is exiting.")


if __name__ == '__main__':
    import sys
    sys.exit(main())