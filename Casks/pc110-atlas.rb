cask "pc110-atlas" do
  arch arm: "arm64", intel: "x64"

  version "1.0.3"
  sha256 arm:   "1a7bbe5d4a9dbd66f926d812f2afcb77f2d04d657f13d9bd0dd3c8c375941bd2",
         intel: "065852b5a51d55e19aee2c64fb57a7f5ec56e9eb6431610dfd064981d390b839"

  url "https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v#{version}/pc110-atlas-#{version}-macos-#{arch}.dmg"
  name "PC110 Atlas"
  desc "Interactive companion and emulator for the IBM Palm Top PC 110"
  homepage "https://github.com/ahmadexp/homebrew-pc110-atlas"

  depends_on macos: ">= :monterey"

  app "PC110 Atlas.app"

  zap trash: "~/Library/Application Support/PC110 Atlas"
end
