print("Hello '%s' from %s" % ("Steffy", "Emily"))

print("Hello {} from {}".format("Steffy", "Emily"))
print("Hello {0} from {1}".format("Steffy", "Emily"))
print("Hello {0} from {1}. {0} are you there?".format("Steffy", "Emily"))
print("Hello {to_name} from {from_name}".format(
  to_name="Steffy",
  from_name="Emily"
))

to_name = "Steffy"
from_name = "Emily"
print(f"Hello {to_name} from {from_name}")

print("""
Hey %s!
Multiline works too!
""" % "Steffy"
)

print("Hello '"+"Steffy"+"' from %s" % ("Steffy", "Emily"))