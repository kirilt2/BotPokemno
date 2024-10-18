local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local DuckCoinsDataStore = DataStoreService:GetDataStore("DuckCoinsStore")


local function parseAbbreviatedValue(input)
    local suffix = input:sub(-1)  -- The last character (e.g., K, M, B, etc.)
    local numberPart = tonumber(input:sub(1, -2))  -- The numeric part (e.g., 10 in '10K')

    if not numberPart then  -- If number part is invalid, return nil
        return nil
    end

    if suffix == "K" or suffix == "k" then
        return numberPart * 1e3  -- Thousands
    elseif suffix == "M" or suffix == "m" then
        return numberPart * 1e6  -- Millions
    elseif suffix == "B" or suffix == "b" then
        return numberPart * 1e9  -- Billions
    elseif suffix == "T" or suffix == "t" then
        return numberPart * 1e12 -- Trillions
    elseif suffix == "Q" or suffix == "q" then
        return numberPart * 1e15 -- Quadrillions
    elseif suffix == "S" or suffix == "s" then
        return numberPart * 1e18 -- Septillions (1e18)
    else
        return tonumber(input)  -- If no suffix, just return the number
    end
end

-- Function to format large numbers into readable strings
local function formatCoins(value)
    if value >= 1e18 then
        return string.format("%.1fS", value / 1e18)  -- Septillions
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
        return tostring(value)
    end
end

-- Updates the DuckCoins GUI
local function updateDuckCoinsGUI(player, amount)
    local playerGui = player:WaitForChild("PlayerGui")
    local coinsGui = playerGui:WaitForChild("CoinsGUI")
    local backGround = coinsGui:WaitForChild("BackGround")
    local textCoins = backGround:WaitForChild("Count")

    textCoins.Text = "DuckCoins: " .. formatCoins(amount)
end

-- Finds a player by partial username
local function findPlayerByPartialName(partialName)
    for _, player in ipairs(Players:GetPlayers()) do
        if player.Name:lower():sub(1, partialName)
            return player
        end
    end
    return nil
end

-- Gives DuckCoins to a player
local function giveDuckCoins(username, amount)
    local player = findPlayerByPartialName(username)
    if player then
        local leaderstats = player:FindFirstChild("leaderstats")
        if leaderstats then
            local duckCoins = leaderstats:FindFirstChild("DuckCoins")
            if duckCoins then
                duckCoins.Value = duckCoins.Value + amount

                local success, err = pcall(function()
                    DuckCoinsDataStore:SetAsync(player.UserId, duckCoins.Value)
                end)
                if not success then
                    warn("Failed to save DuckCoins for player: " .. player.Name .. " | Error: " .. err)
                end

                updateDuckCoinsGUI(player, duckCoins.Value)

                print(player.Name .. " has been given " .. formatCoins(amount) .. " DuckCoins.")
            end
        end
    else
        print("Player not found: " .. username)
    end
end

-- Removes all DuckCoins from a player
local function removeDuckCoins(username)
    local player = findPlayerByPartialName(username)
    if player then
        local leaderstats = player:FindFirstChild("leaderstats")
        if leaderstats then
            local duckCoins = leaderstats:FindFirstChild("DuckCoins")
            if duckCoins then
                duckCoins.Value = 0

                local success, err = pcall(function()
                    DuckCoinsDataStore:SetAsync(player.UserId, 0)
                end)
                if not success then
                    warn("Failed to save DuckCoins for player: " .. player.Name .. " | Error: " .. err)
                end

                updateDuckCoinsGUI(player, duckCoins.Value)

                print("All DuckCoins have been removed from " .. player.Name .. ".")
            end
        end
    else
        print("Player not found: " .. username)
    end
end


local function hasPermission(player)
    local groupId = 33501971
    local requiredRank = 254
    return player:IsInGroup(groupId) and player:GetRankInGroup(groupId) >= requiredRank
end

-- Handles player commands
local function handleCommand(player, command)
    if hasPermission(player) then
        local args = command:split(" ")
        local action = args[1]:lower()
        local username = args[2]
        local countInput = args[3]

        if action == "/g" and username and countInput then
            local amount = parseAbbreviatedValue(countInput)
            if amount then
                giveDuckCoins(username, amount)
            else
                print("Invalid amount format: " .. countInput)
            end
        elseif action == "/r" and username then
            removeDuckCoins(username)
        else
            print("Invalid command or parameters.")
        end
    else
        print(player.Name .. " does not have permission to use this command.")
    end
end


Players.PlayerAdded:Connect(function(player)
    player.Chatted:Connect(function(message)
        handleCommand(player, message)
    end)
end)
