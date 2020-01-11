from jirafs import exceptions, utils
from jirafs.plugin import CommandPlugin


class Command(CommandPlugin):
    """ Commit local changes for later submission to JIRA """

    MIN_VERSION = "2.0.0"
    MAX_VERSION = "3.0.0"

    def handle(self, args, folder, **kwargs):
        return self.cmd(folder, args.message, *args.git_arguments)

    def add_arguments(self, parser):
        parser.add_argument("-m", "--message", dest="message", default="Untitled")
        parser.add_argument("git_arguments", nargs="*")

    def main(self, folder, message, *args):
        original_hash = folder.run_git_command("rev-parse", "master")
        folder.status()  # To trigger macro execution
        folder.run_git_command("add", "-A")
        try:
            folder.run_git_command("commit", "-m", message, *args)
            final_hash = folder.run_git_command("rev-parse", "master")
            folder.log("Changes committed; current hash is %s" % final_hash)
        except exceptions.GitCommandError:
            print("Nothing to commit")
        final_hash = folder.run_git_command("rev-parse", "master")
        return utils.PostStatusResponse(original_hash == final_hash, final_hash)
