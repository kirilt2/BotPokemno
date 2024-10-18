local ReplicatedStorage = game:GetService("ReplicatedStorage")
local player = game.Players.LocalPlayer
local leaderstats = player:FindFirstChild("leaderstats")
local duckCoins = leaderstats and leaderstats:FindFirstChild("DuckCoins")  

local UpdateGUI = player.PlayerGui:WaitForChild("UpdatesGUI")
local Background = UpdateGUI:WaitForChild("BackGround")
local Update1Frame = Background:WaitForChild("MoreDuckCoinsUpdateFarme")
local BuyButton = Update1Frame:WaitForChild("BuyButton")
local playerGui = player:WaitForChild("PlayerGui")

UpdateGUI.Enabled = true

local function formatCoins(value)
	if value == nil then return "0" end  
	if value >= 1e18 then
		return string.format("%.1fO", value / 1e18)  -- Octillions
	elseif value >= 1e15 then
		return string.format("%.1fS", value / 1e15)  -- Septillions
	elseif value >= 1e12 then
		return string.format("%.1fQX", value / 1e12)  -- Quintillions
	elseif value >= 1e15 then
		return string.format("%.1fQ", value / 1e15)  -- Quadrillions
	elseif value >= 1e12 then
		return string.format("%.1fT", value / 1e12)  -- Trillions
	elseif value >= 1e9 then
		return string.format("%.1fB", value / 1e9)   -- Billions
	elseif value >= 1e6 then
		return string.format("%.1fM", value / 1e6)   -- Millions
	elseif value >= 1e3 then
		return string.format("%.1fK", value / 1e3)   -- Thousands
	else
		return tostring(value)  -- Less than 1,000
	end 
end

local buyItemEvent = ReplicatedStorage:WaitForChild("BuyItemEvent")

local currentPrice = 3 
local maxPrice = 1e18   
BuyButton.Text = formatCoins(currentPrice)  

local function onBuyButtonClick()

	if duckCoins and duckCoins.Value >= currentPrice then
		buyItemEvent:FireServer(currentPrice)  
	else
	
		BuyButton.Text = "Max"  
		BuyButton.Active = false  
		BuyButton.AutoButtonColor = false 
	end
end

local function updateButtonText(newPrice)
	if newPrice == nil or newPrice > maxPrice then
		currentPrice = nil  
		BuyButton.Text = "Max"  
		BuyButton.Active = false  
		BuyButton.AutoButtonColor = false 
	else
		currentPrice = newPrice or currentPrice  
		BuyButton.Text = formatCoins(currentPrice)  
		BuyButton.Active = true  
		BuyButton.AutoButtonColor = true 
	end

	local StartGui = playerGui:FindFirstChild("CoinsGUI")
	if StartGui then
		local Background = StartGui:FindFirstChild("BackGround")
		local TextCoins = Background and Background:FindFirstChild("Count")

		if TextCoins and duckCoins then
			TextCoins.Text = "DuckCoins: " .. formatCoins(duckCoins.Value or 0)  
		end
	end
end

BuyButton.MouseButton1Click:Connect(onBuyButtonClick)
buyItemEvent.OnClientEvent:Connect(updateButtonText)
