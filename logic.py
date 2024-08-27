
local player = game.Players.LocalPlayer
local gamePassID = 32123423423 
local textLabel = script.Parent.Parent.TextLabel
local textButton = script.Parent

local function updateGamePassStatus()
    if player:HasPass(gamePassID) then
        textLabel.Text = "Owned"
        textButton.Visible = false
    else
        textLabel.Text = "Buy Max Admin (EARLY ACCESS)"
        textButton.Visible = true
    end
end

textButton.MouseButton1Click:Connect(function()
    if not player:HasPass(gamePassID) then
        game:GetService("MarketplaceService"):PromptGamePassPurchase(player, gamePassID)
    end
end)

updateGamePassStatus()
