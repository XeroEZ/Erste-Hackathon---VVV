import { images } from "@/constants/images";
import { Text, View, Image } from "react-native";

export default function Index() {
  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />
    </View>
  );
}
