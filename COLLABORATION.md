# Repository collaboration setup

This guide explains how a collaborator can contribute over SSH, including when
their computer has access to multiple GitHub accounts.

The commands use these anonymized example values; replace them with the real
values before running a command:

| Placeholder | Example meaning |
|---|---|
| `your-github-username` | Collaborator's GitHub username |
| `you@example.com` | Email verified by that GitHub account |
| `repository-owner` | User or organization that owns the repository |
| `repository-name` | Repository name |
| `github-collaborator` | Local SSH alias |

## 1. Repository owner: invite the collaborator

In GitHub, open the repository and go to:

```text
Settings → Collaborators → Add people
```

Invite the collaborator's GitHub username. The collaborator must accept the invitation before
they can push. An invitation grants repository access to a GitHub account; it
does not configure that account on their computer.

## 2. Collaborator: configure commit identity

Run these commands inside the cloned repository:

```bash
git config user.name "your-github-username"
git config user.email "you@example.com"
```

These local settings control commit authorship. They do not select the SSH key
used to authenticate a push. Use an email verified by GitHub, or the private
`noreply` email shown in GitHub email settings, if commits should appear on the
correct profile.

Check the result:

```bash
git config --get user.name
git config --get user.email
```

## 3. Create or select an SSH key

First inspect existing public keys:

```bash
ls -al ~/.ssh
```

If none belongs to the collaborator's account, create a dedicated key. The explicit
filename avoids overwriting an existing key:

```bash
ssh-keygen -t ed25519 \
  -C "you@example.com" \
  -f ~/.ssh/id_ed25519_collaborator
```

The private key has no `.pub` suffix and must remain secret. Only the public
key may be uploaded:

```text
Private: ~/.ssh/id_ed25519_collaborator
Public:  ~/.ssh/id_ed25519_collaborator.pub
```

## 4. Register the public key with GitHub

On macOS, copy it with:

```bash
pbcopy < ~/.ssh/id_ed25519_collaborator.pub
```

On Linux, print it and copy the complete line:

```bash
cat ~/.ssh/id_ed25519_collaborator.pub
```

While signed in to GitHub as the collaborator's account, go to:

```text
Settings → SSH and GPG keys → New SSH key
```

Add the public key as an **Authentication Key**. A key registered to a different
GitHub account authenticates as that other account regardless of the Git remote
owner or local `user.name`.

## 5. Configure an SSH alias

Add this entry to `~/.ssh/config`:

```sshconfig
Host github-collaborator
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_collaborator
    IdentitiesOnly yes
    AddKeysToAgent yes
    IgnoreUnknown UseKeychain
    UseKeychain yes
```

`github-collaborator` is a local example name and does not need to match a GitHub username.
`IdentitiesOnly yes` is important when the SSH agent contains multiple keys: it
prevents another account's key from being offered first.

`IgnoreUnknown UseKeychain` keeps this block portable: macOS can use its
keychain integration, while SSH implementations without `UseKeychain` ignore
that option.

Protect the configuration and private key:

```bash
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/id_ed25519_collaborator
```

## 6. Load and verify the key

On macOS:

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519_collaborator
```

On Linux:

```bash
ssh-add ~/.ssh/id_ed25519_collaborator
```

Test the alias before using Git:

```bash
ssh -T git@github-collaborator
```

The response must identify the collaborator's GitHub username. GitHub's message that it does
not provide shell access is expected.

## 7. Clone or update the repository remote

For a new clone:

```bash
git clone \
  git@github-collaborator:repository-owner/repository-name.git
```

For an existing clone:

```bash
git remote set-url origin \
  git@github-collaborator:repository-owner/repository-name.git
```

Verify that the alias—not `github.com`—appears in both URLs:

```bash
git remote -v
```

Then push the branch:

```bash
git push --set-upstream origin main
```

## Common failures

### `Author identity unknown`

This is a commit-metadata problem, not SSH authentication. Repeat step 2 inside
the repository.

### `Permission denied to <owner>/<repository> for <unexpected-user>`

SSH authenticated another GitHub account. Check:

```bash
ssh -T git@github-collaborator
ssh -G github-collaborator | grep -E '^(hostname|user|identityfile|identitiesonly) '
git remote -v
```

Confirm that the host alias is used in the remote, the intended identity file is
selected, and `IdentitiesOnly` is `yes`.

### `Permission denied (publickey)`

Confirm that the public key was added to the intended GitHub account and that
the private key is loaded:

```bash
ssh-add -l
ssh -T git@github-collaborator
```

### Authentication succeeds, but push is rejected

Confirm that the invitation was accepted and the authenticated account has
write access. A protected branch may also require pushing a feature branch and
opening a pull request:

```bash
git switch -c feature/my-change
git push --set-upstream origin feature/my-change
```

## Security rules

- Never commit or share a private SSH key.
- Never send a private key through chat, email, or a ticket.
- Use a distinct key when separating GitHub identities.
- Protect keys with passphrases and use the operating system's key agent.
- Remove obsolete keys from GitHub and from the local SSH agent.
- Grant collaborators only the repository permissions they need.

## References

- [GitHub: Connecting with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [GitHub: Add a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- [GitHub: Manage multiple accounts](https://docs.github.com/en/account-and-profile/how-tos/account-management/managing-multiple-accounts)
