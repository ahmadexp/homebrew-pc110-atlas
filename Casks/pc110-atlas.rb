cask "pc110-atlas" do
  arch arm: "arm64", intel: "x64"

  version "1.0.0"
  sha256 arm:   "d93fbde179b16b488f71b19d9424afb807241c6dcea8c44957cf3d6fca90d3c9",
         intel: "338bb7e5b9344d2a8b956b5d36fb60e09e4c06f326111019c15f164f34fd102c"

  url "https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v#{version}/pc110-atlas-#{version}-macos-#{arch}.dmg"
  name "PC110 Atlas"
  desc "Interactive companion and emulator for the IBM Palm Top PC 110"
  homepage "https://github.com/ahmadexp/homebrew-pc110-atlas"

  depends_on macos: ">= :monterey"

  app "PC110 Atlas.app"

  zap trash: "~/Library/Application Support/PC110 Atlas"
end
