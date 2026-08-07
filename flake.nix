{
  description = "An empty canvas.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-26.05";
  };

  outputs = { self, nixpkgs, ... }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in {
    devShells.${system} = {
      default = pkgs.mkShell {
      
      # Install packages from nixpkgs
	packages = with pkgs; [
	  # Python
	  python314
	]++ (with pkgs.python314Packages; [
	  # Dependencies
            uvicorn
	    fastapi
	    sqlalchemy
	    pillow
	]);

	# Install all dependencies of a package
#        inputsFrom = with pkgs; [];

	# Commands run before starting the shell
	shellHook = ''
	  python --version
          uvicorn --version
	'';

	# Enviroment variables
#        ENVVAR = "value";
      };
    };
  };
}
