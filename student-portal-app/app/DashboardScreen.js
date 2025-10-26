import React, { useEffect, useState } from "react";
import { View, Text, Button, ScrollView, StyleSheet } from "react-native";
import { api } from "../api/client";

export default function DashboardScreen({ route, navigation }) {
  const { token } = route.params;
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await api.get("dashboard/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setData(res.data);
      } catch (err) {
        console.log(err);
      }
    };
    fetchDashboard();
  }, []);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>📘 Dashboard</Text>
      {data ? (
        <View>
          <Text>Name: {data.profile?.name}</Text>
          <Text>Role: {data.profile?.role}</Text>
          <Text>Courses: {data.courses?.length}</Text>
        </View>
      ) : (
        <Text>Loading...</Text>
      )}
      <Button title="Logout" onPress={() => navigation.goBack()} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 22, fontWeight: "bold", marginBottom: 10 },
});
