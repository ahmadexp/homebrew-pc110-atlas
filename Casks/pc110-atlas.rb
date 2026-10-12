cask "pc110-atlas" do
  arch arm: "arm64", intel: "x64"

  version "1.0.2"
  sha256 arm:   "382437cb5af43cec48708463851126a88885a349d14ecc1cc5223e7c102bb649",
         intel: "676155ead9ce089b04035f62321af77e2eb3707aa1e3f7fb41350d18ad4e320b"

  url "https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v#{version}/pc110-atlas-#{version}-macos-#{arch}.dmg"
  name "PC110 Atlas"
  desc "Interactive companion and emulator for the IBM Palm Top PC 110"
  homepage "https://github.com/ahmadexp/homebrew-pc110-atlas"

  depends_on macos: ">= :monterey"

  app "PC110 Atlas.app"

  zap trash: "~/Library/Application Support/PC110 Atlas"
end
