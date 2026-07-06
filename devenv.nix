{ pkgs, ... }:

{
  languages.python = {
    enable = true;
    version = "3.12";
    uv = {
      enable = true;
      sync.enable = true;
    };
  };

  packages = [
    pkgs.mesa
    pkgs.libGL
    pkgs.libx11
    pkgs.xorg.libXrender
    pkgs.expat
    pkgs.zlib
  ];
}
