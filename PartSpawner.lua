-- Services
local TweenService = game:GetService("TweenService") -- Service to handle tweens
local Players = game:GetService("Players") -- Service to manage players
local ReplicatedStorage = game:GetService("ReplicatedStorage") -- Service to store replicated data
local Workspace = game:GetService("Workspace") -- Service to manage game workspace
local UserInputService = game:GetService("UserInputService") -- Service to manage user input
local RunService = game:GetService("RunService") -- Service for running functions on game loop

-- Constants and Configurations
local COINS_PER_PART = 1 -- Coins given per part collected
local BONUS_COINS = 2 -- Bonus coins every 30 seconds
local COINS_RESET_TIME = 120 -- Time in seconds to reset coins
local PART_SPAWN_INTERVAL = 5 -- Interval between part spawns
local MIN_PART_SIZE = 1 -- Minimum size of spawned parts
local MAX_PART_SIZE = 3 -- Maximum size of spawned parts
local COIN_NOTIFY_EVENT = Instance.new("CoinsNot") -- Remote event for coin notifications

-- Variables
local gameDuration = 0 -- Timer for the game duration
local spawnCooldown = false -- Cooldown flag for spawning
local SpawnPart = Workspace:WaitForChild("SpawnPart") -- The part where new parts will spawn
local OutPart = Workspace:WaitForChild("OutPart") -- The destination part
local TweenedParts = {} -- Table to store tweened parts

-- Function to setup player leaderboards
local function setupLeaderboards(player)
	local leaderstats = Instance.new("Folder") -- Create a new folder for leaderstats
	leaderstats.Name = "leaderstats" -- Name it leaderstats
	leaderstats.Parent = player -- Parent to the player

	local coins = Instance.new("IntValue") -- Create an IntValue for coins
	coins.Name = "Coins" -- Name it Coins
	coins.Value = 0 -- Initialize to 0
	coins.Parent = leaderstats -- Parent to leaderstats
end

-- Function to update game timer
local function updateGameTimer()
	while true do
		gameDuration += 1 -- Increment game duration every second
		wait(1) -- Wait for 1 second
	end
end

-- Function to spawn parts
local function spawnPart()
	if spawnCooldown then return end -- Exit if in cooldown

	spawnCooldown = true -- Set cooldown
	local newPart = Instance.new("Part") -- Create a new part
	newPart.Size = Vector3.new(math.random(MIN_PART_SIZE, MAX_PART_SIZE), math.random(MIN_PART_SIZE, MAX_PART_SIZE), math.random(MIN_PART_SIZE, MAX_PART_SIZE)) -- Random size
	newPart.Position = SpawnPart.Position + Vector3.new(0, 5, 0) -- Spawn above the SpawnPart
	newPart.Anchored = true -- Anchor the part while we set it up
	newPart.BrickColor = BrickColor.Random() -- Give it a random color
	newPart.Parent = Workspace -- Parent the part to the workspace

	-- Tween properties
	local tweenInfo = TweenInfo.new(2, Enum.EasingStyle.Quad, Enum.EasingDirection.Out) -- Tweening style and duration
	local goal = {Position = OutPart.Position + Vector3.new(0, 1, 0)} -- Move to just above OutPart

	local tween = TweenService:Create(newPart, tweenInfo, goal) -- Create the tween
	tween:Play() -- Play the tween
	tween.Completed:Wait() -- Wait until the tween is finished

	-- Check for players to give coins
	for _, player in ipairs(Players:GetPlayers()) do
		local leaderstats = player:FindFirstChild("leaderstats") -- Find the leaderstats folder
		if leaderstats then
			local coins = leaderstats:FindFirstChild("Coins") -- Find the Coins value
			if coins then
				coins.Value += COINS_PER_PART -- Give 1 coin
				COIN_NOTIFY_EVENT:FireClient(player, coins.Value) -- Notify the player of their new coin count
			end
		end
	end

	newPart:Destroy() -- Destroy the part after the animation
	spawnCooldown = false -- Reset cooldown
end

-- Function to spawn multiple parts at once
local function spawnMultipleParts(count)
	for i = 1, count do
		spawnPart()
		wait(0.5) -- Delay between spawning multiple parts
	end
end

-- Function to increase spawn rate over time
local function increaseSpawnRate()
	while true do
		if PART_SPAWN_INTERVAL > 1 then
			PART_SPAWN_INTERVAL -= 0.5 -- Decrease interval to increase spawn rate
		end
		wait(30) -- Wait 30 seconds before next increase
	end
end

-- Function to reset player coins
local function resetPlayerCoins(player)
	local leaderstats = player:FindFirstChild("leaderstats")
	if leaderstats then
		local coins = leaderstats:FindFirstChild("Coins")
		if coins then
			coins.Value = 0 -- Reset coins to zero
		end
	end
end

-- Function to track game duration and reset when necessary
local function trackGameDuration()
	while true do
		if gameDuration >= COINS_RESET_TIME then -- If game duration reaches reset time
			for _, player in ipairs(Players:GetPlayers()) do
				resetPlayerCoins(player) -- Reset player coins
			end
			gameDuration = 0 -- Reset the timer
		end
		wait(10) -- Check every 10 seconds
	end
end

-- Function to log player actions
local function logPlayerAction(player, action)
	print(player.Name .. " performed action: " .. action) -- Log action to console
end

-- Function to give bonus coins based on game duration
local function giveBonusCoins()
	while true do
		for _, player in ipairs(Players:GetPlayers()) do
			local leaderstats = player:FindFirstChild("leaderstats")
			if leaderstats then
				local coins = leaderstats:FindFirstChild("Coins")
				if coins then
					if gameDuration % 30 == 0 and gameDuration > 0 then -- Every 30 seconds
						coins.Value += BONUS_COINS -- Give 2 bonus coins
						logPlayerAction(player, "Received 2 bonus coins!") -- Log the action
						COIN_NOTIFY_EVENT:FireClient(player, coins.Value) -- Notify player
					end
				end
			end
		end
		wait(10) -- Wait before checking again
	end
end

-- Function to handle player joining
local function onPlayerAdded(player)
	setupLeaderboards(player) -- Set up leaderboards for the new player
end

-- Connect player added event
Players.PlayerAdded:Connect(onPlayerAdded)

-- Setup GUI for notifications
local function setupNotificationGui(player)
	local playerGui = player:WaitForChild("PlayerGui")

	local screenGui = Instance.new("ScreenGui")
	screenGui.Name = "CoinNotificationGui"
	screenGui.Parent = playerGui

	local notificationFrame = Instance.new("Frame")
	notificationFrame.Size = UDim2.new(0.3, 0, 0.1, 0)
	notificationFrame.Position = UDim2.new(0.35, 0, 0, 0)
	notificationFrame.BackgroundColor3 = Color3.fromRGB(0, 170, 0)
	notificationFrame.BackgroundTransparency = 0.5
	notificationFrame.Visible = false
	notificationFrame.Parent = screenGui

	local notificationText = Instance.new("TextLabel")
	notificationText.Size = UDim2.new(1, 0, 1, 0)
	notificationText.TextColor3 = Color3.new(1, 1, 1)
	notificationText.BackgroundTransparency = 1
	notificationText.TextScaled = true
	notificationText.Parent = notificationFrame

	-- Function to show the notification
	local function showNotification(coinCount)
		notificationText.Text = "You received a coin! Total Coins: " .. coinCount
		notificationFrame.Visible = true

		-- Animate the notification
		local tweenIn = TweenService:Create(notificationFrame, TweenInfo.new(0.5), {Position = UDim2.new(0.35, 0, 0.2, 0)})
		local tweenOut = TweenService:Create(notificationFrame, TweenInfo.new(0.5), {Position = UDim2.new(0.35, 0, 0, 0)})

		tweenIn:Play()
		tweenIn.Completed:Wait() -- Wait for the tween in to finish
		wait(1) -- Wait for a second before tweening out
		tweenOut:Play()
		tweenOut.Completed:Wait() -- Wait for the tween out to finish
		notificationFrame.Visible = false
	end

	-- Connect the notification function to the event
	COIN_NOTIFY_EVENT.OnClientEvent:Connect(showNotification)
end

-- Setup a notification system for all players
Players.PlayerAdded:Connect(function(player)
	setupNotificationGui(player) -- Set up notification GUI for each player
end)

-- Start all necessary coroutines
coroutine.wrap(updateGameTimer)()
coroutine.wrap(increaseSpawnRate)()
coroutine.wrap(trackGameDuration)()
coroutine.wrap(giveBonusCoins)()

-- Main game loop to spawn parts
while true do
	spawnMultipleParts(2) -- Spawn 2 parts every cycle
	wait(PART_SPAWN_INTERVAL) -- Wait for the specified spawn interval
end
