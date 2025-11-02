import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  TextInput,
  Button,
  ScrollView,
  StyleSheet,
  Alert,
  TouchableOpacity,
} from "react-native";
import { fetchProfiles, createProfile, deleteProfile } from "../api/client";

export default function ManageUsersScreen({ route, navigation }) {
  const { token } = route.params;
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newUser, setNewUser] = useState({
    username: "",
    email: "",
    password: "",
    name: "",
    role: "student",
  });

  // Load all users
  useEffect(() => {
    const loadProfiles = async () => {
      try {
        const res = await fetchProfiles(token);
        setProfiles(res);
      } catch (err) {
        Alert.alert("Error", "Failed to load users.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadProfiles();
  }, []);

  // Add new user
  const handleAddUser = async () => {
    if (!newUser.username || !newUser.password) {
      return Alert.alert("Missing Info", "Username and password are required.");
    }
    try {
      await createProfile(token, newUser);
      Alert.alert("Success", "User created successfully!");
      setNewUser({ username: "", email: "", password: "", name: "", role: "student" });
      const refreshed = await fetchProfiles(token);
      setProfiles(refreshed);
    } catch (err) {
      console.error(err);
      Alert.alert("Error", "Failed to create user.");
    }
  };

  // Delete user
  const handleDeleteUser = async (id) => {
    Alert.alert("Confirm Delete", "Are you sure?", [
      { text: "Cancel" },
      {
        text: "Delete",
        onPress: async () => {
          try {
            await deleteProfile(token, id);
            Alert.alert("Deleted", "User removed.");
            setProfiles((prev) => prev.filter((p) => p.id !== id));
          } catch (err) {
            console.error(err);
            Alert.alert("Error", "Failed to delete user.");
          }
        },
      },
    ]);
  };

  if (loading) return <Text>Loading users...</Text>;

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>👥 Manage Users</Text>

      {/* Add new user form */}
      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Create New User</Text>
        <TextInput
          placeholder="Username"
          style={styles.input}
          value={newUser.username}
          onChangeText={(t) => setNewUser({ ...newUser, username: t })}
        />
        <TextInput
          placeholder="Email"
          style={styles.input}
          value={newUser.email}
          onChangeText={(t) => setNewUser({ ...newUser, email: t })}
        />
        <TextInput
          placeholder="Password"
          secureTextEntry
          style={styles.input}
          value={newUser.password}
          onChangeText={(t) => setNewUser({ ...newUser, password: t })}
        />
        <TextInput
          placeholder="Full Name"
          style={styles.input}
          value={newUser.name}
          onChangeText={(t) => setNewUser({ ...newUser, name: t })}
        />
        <TextInput
          placeholder="Role (student / lecturer / admin)"
          style={styles.input}
          value={newUser.role}
          onChangeText={(t) => setNewUser({ ...newUser, role: t.toLowerCase() })}
        />
        <Button title="Add User" onPress={handleAddUser} />
      </View>

      {/* List all users */}
      <Text style={[styles.sectionTitle, { marginTop: 20 }]}>Existing Users</Text>
      {profiles.length === 0 ? (
        <Text>No users found.</Text>
      ) : (
        profiles.map((p) => (
          <View key={p.id} style={styles.userCard}>
            <View>
              <Text style={styles.username}>{p.name || p.user?.username}</Text>
              <Text>Role: {p.role}</Text>
              <Text>Email: {p.user?.email}</Text>
            </View>
            <TouchableOpacity
              style={styles.deleteButton}
              onPress={() => handleDeleteUser(p.id)}
            >
              <Text style={{ color: "#fff" }}>Delete</Text>
            </TouchableOpacity>
          </View>
        ))
      )}

      <Button title="⬅ Back to Dashboard" onPress={() => navigation.goBack()} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: "#fff" },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 15 },
  sectionTitle: { fontSize: 18, fontWeight: "600", marginBottom: 10 },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 10,
    borderRadius: 8,
    marginBottom: 10,
  },
  card: {
    padding: 15,
    backgroundColor: "#f2f2f2",
    borderRadius: 10,
    marginBottom: 15,
  },
  userCard: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#ddd",
    padding: 10,
    borderRadius: 10,
    marginBottom: 10,
  },
  username: { fontWeight: "bold", fontSize: 16 },
  deleteButton: {
    backgroundColor: "red",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
});
