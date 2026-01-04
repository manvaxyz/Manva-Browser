FROM golang:1.21-alpine AS build
WORKDIR /src
COPY . .
RUN go build -o /bin/update-service main.go

FROM alpine:3.18
COPY --from=build /bin/update-service /bin/update-service
EXPOSE 8082
ENTRYPOINT ["/bin/update-service"]
