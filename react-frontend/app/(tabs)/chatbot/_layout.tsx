import { Tabs } from "expo-router";
import { View, Image, ImageBackground } from "react-native";
import { images } from "@/constants/images";
import { icons } from "@/constants/icons";

const TabIcon = ({ focused, icon }: any) => {
  if (focused) {
    return (
      <ImageBackground
        source={images.highlight}
        className="flex flex-row w-full flex-1 min-w-[80px] min-h-14 mt-4 justify-center items-center rounded-full overflow-hidden"
      >
        <Image source={icon} tintColor="#FFFFFF" className="size-8" />
      </ImageBackground>
    );
  }
  return (
    <View className="size-full justify-center items-center mt-4 rounded-full">
      <Image source={icon} tintColor="#8D8D8D" className="size-8" />;
    </View>
  );
};

const _layout = () => {
  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      <Tabs
        screenOptions={{
          tabBarShowLabel: false,
          tabBarStyle: {
            backgroundColor: "#272727",
            borderRadius: 70,
            marginHorizontal: 20,
            marginTop: 40,
            height: 53,
            position: "absolute",
            overflow: "hidden",
            top: 0,
            borderWidth: 0.5,
            borderColor: "#898989",
          },
          tabBarItemStyle: {
            width: "100%",
            height: "100%",
            justifyContent: "center",
            alignItems: "center",
          },
          headerShown: false,
        }}
      >
        <Tabs.Screen
          name="chat"
          options={{
            title: "Chat",
            tabBarIcon: ({ focused }) => (
              <TabIcon focused={focused} icon={icons.chatbot} />
            ), // No icons for nested tabs
          }}
        />
        <Tabs.Screen
          name="history"
          options={{
            title: "History",
            tabBarIcon: ({ focused }) => (
              <TabIcon focused={focused} icon={icons.history} />
            ),
          }}
        />
      </Tabs>
    </View>
  );
};

export default _layout;
