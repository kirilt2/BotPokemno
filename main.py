local showPartsEvent = game.ReplicatedStorage:WaitForChild("ShowPartsEvent")

showPartsEvent.OnClientEvent:Connect(function(show)
    local folder = workspace:WaitForChild("PartShow")
    for _, obj in pairs(folder:GetChildren()) do
        if obj:IsA("BasePart") then
            if show then
                obj.Transparency = 0 
            else
                obj.Transparency = 1 
            end
        end
    end
end)
