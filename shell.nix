{ pkgs ? import <nixpkgs> { } }:
let
  basePackages = with pkgs; [
    nixfmt
    # Despite supported systems including darwin, it appears broken on darwin.
    micropython
  ];
  pythonPackages = with pkgs.python310Packages; [ autopep8 ];
in pkgs.mkShell {
  name = "nix-config";
  buildInputs = basePackages ++ pythonPackages;
  shellHook = "";
}
