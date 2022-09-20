{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  name = "nix-config";
  # https://micropython.org/download/rp2-pico-w/rp2-pico-w-latest.uf2
  buildInputs = with pkgs; [
    nixfmt
    micropython
    yapf
  ];
  shellHook = "";
}
