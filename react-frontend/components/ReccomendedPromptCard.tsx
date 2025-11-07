import { View, Text, TouchableOpacity } from "react-native";
import React from "react";
import { router } from "expo-router";

interface ReccomendedPromptCardProps {
  prompt: string;
  color: "blue" | "red" | "green" | "pink";
  onPress?: () => void;
}

const ReccomendedPromptCard = ({
  prompt,
  color,
  onPress,
}: ReccomendedPromptCardProps) => {
  const handlePress = () => {
    if (onPress) {
      onPress();
    } else {
      // TODO: Navigate to new chat with this prompt
      // const chatId = generateNewChatId(); // You'll implement this
      // router.push(`/chats/${chatId}?prompt=${encodeURIComponent(prompt)}`);
      console.log("Navigate to new chat with prompt:", prompt);
    }
  };

  const getColorClass = () => {
    switch (color) {
      case "blue":
        return "bg-card-blue";
      case "red":
        return "bg-card-red";
      case "green":
        return "bg-card-green";
      case "pink":
        return "bg-card-pink";
      default:
        return "bg-card-blue";
    }
  };

  return (
    <TouchableOpacity
      className={`${getColorClass()} p-4 rounded-xl min-h-[100px] justify-center items-center mx-2 my-2 shadow-lg`}
      onPress={handlePress}
      activeOpacity={0.8}
    >
      <Text className="text-white text-center font-semibold text-sm leading-5">
        {prompt}
      </Text>
    </TouchableOpacity>
  );
};

export default ReccomendedPromptCard;
