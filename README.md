# Keypirinha Plugin: pwpush

This is pwpush, a plugin for the
[Keypirinha](http://keypirinha.com) launcher.

This package adds the option to create a secure way to share passwords and/or files using the [pwpush Api](https://pwpush.com/api/1.0.en.html).

![](https://github.com/acetoacetato/keypirinha-PwPush/blob/V1.0.0/resources/intro.gif)


## Download


The built packages can be found on [the repo's releases section](https://github.com/acetoacetato/keypirinha-PwPush/releases)


## Install

Once the `pwpush.keypirinha-package` file is installed,
move it to the `InstalledPackage` folder located at:

* `Keypirinha\portable\Profile\InstalledPackages` in **Portable mode**
* **Or** `%APPDATA%\Keypirinha\InstalledPackages` in **Installed mode** (the
  final path would look like
  `C:\Users\%USERNAME%\AppData\Roaming\Keypirinha\InstalledPackages`)


## Usage

The plugin adds one option to the catalog:

   Create Sharing Link (pwpush)

This allows to input a text entry or a file path. In case of a file path is detected, you can choose if creating a link to just the text itself or upload the file.

**IMPORTANT**

In order to upload a file it is needed to configure a api key. For this, you need to open the configuration file and add your pwpush account's email and api key:

   [defaults]
   api_email=<YOUR PWPUSH ACCOUNT EMAIL>
   api_key=<YOUR API KEY>

If configured, it will be used for both the text and file sharing.


## Change Log


### v1.0

* Added initial functionality: Uploading one file or text.


## License

This package is distributed under the terms of the MIT license.



## Contribute


1. Check for open issues or open a fresh issue to start a discussion around a
   feature idea or a bug.
2. Fork this repository on GitHub to start making your changes to the **dev**
   branch.
3. Send a pull request.
4. Add yourself to the *Contributors* section below (or create it if needed)!
