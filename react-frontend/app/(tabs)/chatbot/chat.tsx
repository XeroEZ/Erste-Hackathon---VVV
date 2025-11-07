import { View, Text, Image, KeyboardAvoidingView } from "react-native";
import React, { useState } from "react";
import { images } from "@/constants/images";
import SearchBar from "@/components/SearchBar";
import { KeyboardAwareScrollView } from "react-native-keyboard-aware-scroll-view";
import ReccomendedPromptCard from "@/components/ReccomendedPromptCard";

const chat = () => {
  const [promptValue, setPromptValue] = useState("");

  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      <View>
        <ReccomendedPromptCard
          prompt="What's my account balance?"
          color="blue"
        />
      </View>

      <KeyboardAwareScrollView
        className="flex-1"
        contentContainerStyle={{ flexGrow: 1 }}
        enableOnAndroid={true}
        keyboardShouldPersistTaps="handled"
        extraScrollHeight={150}
      >
        <View className="flex-1 justify-end pb-20 px-5">
          <View className="bg-accent rounded-lg py-3.5 flex flex-row justify-center items-center">
            <SearchBar
              placeholder="Type your message..."
              value={promptValue}
              onChangeText={setPromptValue}
            />
          </View>
        </View>
      </KeyboardAwareScrollView>
    </View>
  );
};

export default chat;
