{
  description = "qwerinope's python scripts";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3Packages;

        buildScript = { name, file, deps }:
          python.buildPythonApplication {
            pname = name;
            version = "1.0";
            src = ./.;
            format = "other";
            propagatedBuildInputs = deps;
            installPhase = ''
              mkdir -p $out/bin
              cp ${file} $out/bin/${name}
              chmod +x $out/bin/${name}
              patchShebangs $out/bin/${name}
            '';
          };

        bandc = buildScript {
          name = "bandc";
          file = ./bandcampExtractor/bandc.py;
          deps = [ python.music-tag ];
        };

        cvfiles = buildScript {
          name = "cvfiles";
          file = ./massFileConverter/cvfiles.py;
          deps = [ pkgs.ffmpeg ];
        };

        allscripts = pkgs.symlinkJoin {
          name = "allscripts";
          paths = [ bandc cvfiles ];
        };
      in {
        packages = {
          inherit bandc cvfiles;
          default = allscripts;
        };
      });
}
