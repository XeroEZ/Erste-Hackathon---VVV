import { icons } from "@/constants/icons";
import React from "react";
import { Image, TextInput, TouchableOpacity, View } from "react-native";

interface Props {
  placeholder: string;
  onPress?: () => void;
  onSend?: () => void; // New prop for send action
  value: string;
  onChangeText: (text: string) => void;
}

const SearchBar = ({ placeholder, onPress, onSend, value, onChangeText }: Props) => {
  const handleSend = () => {
    if (value.trim() && onSend) {
      onSend();
    }
  };

  return (
    <View className="flex-row items-center rounded-full gap-3">
      <View
        className="flex-1 bg-box rounded-full border border-stroke "
        style={{ borderWidth: 0.5 }}
      >
        <TextInput
          onPress={onPress}
          placeholder={placeholder}
          value={value}
          onChangeText={onChangeText}
          placeholderTextColor="#8D8D8D"
          className="flex-1 ml-2 text-white p-5"
          returnKeyType="send"
          onSubmitEditing={handleSend}
        />
      </View>
      <TouchableOpacity onPress={handleSend} disabled={!value.trim()}>
        <View
          className="bg-box p-3 rounded-full border border-stroke"
          style={{
            borderWidth: 0.5,
            opacity: value.trim() ? 1 : 0.5 // Disabled state styling
          }}
        >
          <Image
            source={icons.send}
            className="w-10 h-10 p-5"
            resizeMode="contain"
            tintColor="#E3E3E3"
          />
        </View>
      </TouchableOpacity>
    </View>
  );
};

export default SearchBar;
